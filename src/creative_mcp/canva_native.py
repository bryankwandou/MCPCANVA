"""Build a design natively inside the Canva editor (real Canva text boxes and image elements, no PPTX/PDF import).

Canva's public API cannot add elements to a design, so this drives the logged-in Chrome editor over the
DevTools Protocol, one persistent connection per call. Everything is located through the DOM (aria-labels,
field labels), so it does not depend on screen coordinates or zoom.

Spec format (all units are design pixels):
{
  "title": "Spanduk LCB 2026",
  "width": 3000, "height": 1000,            # used when "design_url" is not given
  "design_url": "https://www.canva.com/design/<id>/edit",   # optional: add to an existing design
  "elements": [
    {"type": "image", "path": "C:/.../bg.png", "x": 0, "y": 0, "w": 3000, "h": 1000},
    {"type": "text", "text": "LCB", "font": "Alfa Slab One", "size": 300, "color": "#14206B", "x": 140, "y": 285}
  ]
}
"""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

from .canva_browser import BASE, _Tab, ensure_chrome

# Adaptive pace for the short UI waits: start at CANVA_SPEED (0.25 = 4x faster than the safe waits), double the
# waits after a failure (busy PC or slow Canva), ease back toward full speed after each success.
import os as _os
SPEED = float(_os.getenv("CANVA_SPEED", "0.25"))
_pace = [SPEED]


def _nap(s):
    time.sleep(s * _pace[0])


def pace_ok():
    _pace[0] = max(SPEED, _pace[0] * 0.85)


def pace_fail():
    _pace[0] = min(1.0, _pace[0] * 2)

_FIELD = """(()=>{const i=[...document.querySelectorAll('input')].find(i=>{const l=i.closest('label')||i.parentElement?.parentElement;
  return (l?.innerText||'').trim().split(String.fromCharCode(10))[0]===%s});if(!i)return null;
  const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,i.value]})()"""
_BTN = """(()=>{const b=[...document.querySelectorAll('button,[role=button],[role=option],[role=tab]')].find(b=>{
  const t=(b.getAttribute('aria-label')||b.innerText||'').trim();return %s});if(!b)return null;
  const r=b.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,b.getAttribute('aria-pressed')]})()"""

# modifier name -> (CDP bit, key, code, windows virtual key)
MODS = {"alt": (1, "Alt", "AltLeft", 18), "ctrl": (2, "Control", "ControlLeft", 17),
        "meta": (4, "Meta", "MetaLeft", 91), "shift": (8, "Shift", "ShiftLeft", 16)}
MOD_ALIASES = {"control": "ctrl", "ctl": "ctrl", "cmd": "meta", "win": "meta", "option": "alt"}
_NAMED = {  # key -> (code, windows virtual key, text)
    "Enter": ("Enter", 13, None),"Escape": ("Escape", 27, None), "Esc": ("Escape", 27, None),
    "Delete": ("Delete", 46, None), "Del": ("Delete", 46, None), "Backspace": ("Backspace", 8, None),
    "Tab": ("Tab", 9, None), "Space": ("Space", 32, " "), " ": ("Space", 32, " "),
    "ArrowLeft": ("ArrowLeft", 37, None), "ArrowUp": ("ArrowUp", 38, None), "ArrowRight": ("ArrowRight", 39, None),
    "ArrowDown": ("ArrowDown", 40, None), "Left": ("ArrowLeft", 37, None), "Up": ("ArrowUp", 38, None),
    "Right": ("ArrowRight", 39, None), "Down": ("ArrowDown", 40, None),
    "Home": ("Home", 36, None), "End": ("End", 35, None), "PageUp": ("PageUp", 33, None), "PageDown": ("PageDown", 34, None),
    "Insert": ("Insert", 45, None),
    **{f"F{i}": (f"F{i}", 111 + i, None) for i in range(1, 13)},
}
# punctuation: key -> (code, vk, shifted key)
_PUNCT = {"=": ("Equal", 187, "+"), "-": ("Minus", 189, "_"), "[": ("BracketLeft", 219, "{"), "]": ("BracketRight", 221, "}"),
          ";": ("Semicolon", 186, ":"), "'": ("Quote", 222, '"'), ",": ("Comma", 188, "<"), ".": ("Period", 190, ">"),
          "/": ("Slash", 191, "?"), "\\": ("Backslash", 220, "|"), "`": ("Backquote", 192, "~")}
_SHIFT_DIGITS = ")!@#$%^&*("
# Chrome editing commands that go with the standard shortcuts (CDP does not run them for synthetic keys otherwise)
EDIT_COMMANDS = {(frozenset({"ctrl"}), "KeyC"): "copy", (frozenset({"ctrl"}), "KeyV"): "paste",
                 (frozenset({"ctrl"}), "KeyX"): "cut", (frozenset({"ctrl"}), "KeyA"): "selectAll",
                 (frozenset({"ctrl"}), "KeyZ"): "undo", (frozenset({"ctrl"}), "KeyY"): "redo",
                 (frozenset({"ctrl", "shift"}), "KeyZ"): "redo"}


def _flat(s) -> str:
    """Text compared without zero-width chars, nbsp or line-break differences."""
    return re.sub(r"\s+", " ", re.sub("[﻿​-‍]", "", s or "").replace(" ", " ")).strip()


def key_spec(k: str, shift: bool = False) -> dict:
    """CDP key fields for one key name ("a", "Z", "7", "=", "Enter", "ArrowLeft", "F5")."""
    if k in _NAMED or k.capitalize() in _NAMED:
        code, vk, text = _NAMED.get(k) or _NAMED[k.capitalize()]
        return {"key": " " if code == "Space" else code, "code": code, "vk": vk, "text": text}
    if len(k) == 1 and k.isalpha():
        return {"key": k.upper() if shift else k.lower(), "code": "Key" + k.upper(), "vk": ord(k.upper()),
                "text": k.upper() if shift else k.lower()}
    if len(k) == 1 and k.isdigit():
        return {"key": _SHIFT_DIGITS[int(k)] if shift else k, "code": "Digit" + k, "vk": ord(k),
                "text": _SHIFT_DIGITS[int(k)] if shift else k}
    if k in _PUNCT:
        code, vk, sk = _PUNCT[k]
        return {"key": sk if shift else k, "code": code, "vk": vk, "text": sk if shift else k}
    raise ValueError(f"tombol tidak dikenal: {k!r}")


class Editor:
    def __init__(self, tab: _Tab):
        self.t = tab
        # style -> text of a box on the current page that already has that style; cleared on page change
        self.styled: dict[tuple, str] = {}
        self.styled_page = None

    # -- low level -------------------------------------------------------------------------------------------
    def click(self, x, y, n=1, button="left"):
        s = self.t.send
        s("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        for i in range(1, n + 1):
            s("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": button, "clickCount": i})
            s("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": button, "clickCount": i})

    def key(self, k, ctrl=False, shift=False, alt=False):
        self.hotkey("+".join([m for m, on in (("ctrl", ctrl), ("shift", shift), ("alt", alt)) if on] + [k]))

    def hotkey(self, combo: str):
        """Press a key combination, e.g. "ctrl+z", "ctrl+shift+z", "shift+ctrl+x", "alt+shift+t", "Delete",
        "ArrowLeft", "F2". Modifiers are held down around the key like a real keyboard, and editing shortcuts
        (copy/paste/cut/undo/redo/select all) also carry Chrome's editing command so text fields react too."""
        parts = [p.strip() for p in combo.replace(" ", "").split("+") if p.strip()]
        if not parts:
            raise ValueError("kombinasi tombol kosong")
        mods = {MOD_ALIASES.get(p.lower(), p.lower()) for p in parts[:-1]}
        bad = mods - set(MODS)
        if bad:
            raise ValueError(f"modifier tidak dikenal: {sorted(bad)}")
        k = parts[-1]
        spec = key_spec(k, "shift" in mods)
        mask = sum(MODS[m][0] for m in mods)
        held = 0
        for m in ("ctrl", "alt", "shift", "meta"):  # press modifiers first
            if m in mods:
                held |= MODS[m][0]
                self.t.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": MODS[m][1], "code": MODS[m][2],
                                                       "windowsVirtualKeyCode": MODS[m][3], "modifiers": held})
        ev = {"key": spec["key"], "code": spec["code"], "windowsVirtualKeyCode": spec["vk"], "modifiers": mask}
        cmd = EDIT_COMMANDS.get((frozenset(mods), spec["code"]))
        self.t.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", **ev, **({"commands": [cmd]} if cmd else {})})
        if spec.get("text") and not (mods & {"ctrl", "alt", "meta"}):
            self.t.send("Input.dispatchKeyEvent", {"type": "char", "text": spec["text"], **ev})
        self.t.send("Input.dispatchKeyEvent", {"type": "keyUp", **ev})
        for m in ("meta", "shift", "alt", "ctrl"):  # release in reverse order
            if m in mods:
                held &= ~MODS[m][0]
                self.t.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": MODS[m][1], "code": MODS[m][2],
                                                       "windowsVirtualKeyCode": MODS[m][3], "modifiers": held})

    # Canva editor shortcuts (Windows). Each one presses the real key combination.
    def undo(self): self.hotkey("ctrl+z")
    def redo(self): self.hotkey("ctrl+y")
    def copy(self): self.hotkey("ctrl+c")
    def paste(self): self.hotkey("ctrl+v")
    def cut(self): self.hotkey("ctrl+x")
    def select_all(self): self.hotkey("ctrl+a")
    def duplicate(self): self.hotkey("ctrl+d")
    def group(self): self.hotkey("ctrl+g")
    def ungroup(self): self.hotkey("ctrl+shift+g")

    def stable_button(self, cond_js: str, wait=20.0):
        """Like button(), but only clicks once the button has stopped moving (carousels, hydrating pages)."""
        end = time.time() + wait
        last = None
        while time.time() < end:
            pos = self.t.ev(_BTN % cond_js)
            if pos and last and abs(pos[0] - last[0]) < 1 and abs(pos[1] - last[1]) < 1:
                self.click(pos[0], pos[1])
                return pos
            last = pos
            _nap(0.7)
        raise RuntimeError(f"tombol tidak ketemu/tidak stabil: {cond_js}")

    def type(self, text):
        self.t.send("Input.insertText", {"text": text})

    def fill_input(self, x, y, value, clicks=1, enter=True, locate=None):
        """Click an <input>, then replace its value. Never sends Ctrl+A: if the click missed the input,
        Ctrl+A would select every element on the page and the next edits would hit all of them.
        `locate` (JS returning [x, y]) re-measures the input between attempts, e.g. while a panel slides in."""
        for attempt in range(3):
            if locate and attempt:
                _nap(0.8)
                p = self.t.ev(locate)
                if p:
                    x, y = p[0], p[1]
            self.click(x, y, clicks)
            _nap(0.25)
            if self.t.ev("""(()=>{const a=document.activeElement;if(!a||!/^(INPUT|TEXTAREA)$/.test(a.tagName))return false;
                a.select();return true})()"""):
                self.type(str(value))
                if enter:
                    self.key("Enter")
                return
            if not locate:
                _nap(0.6)
        self.key("Escape")
        raise RuntimeError(f"kolom input tidak fokus di ({x:.0f},{y:.0f}); dibatalkan")

    def button(self, cond_js: str, wait=8.0):
        """Click the first button whose label/text satisfies cond_js (uses variable t)."""
        pos = self.t.wait(_BTN % cond_js, wait)
        if not pos:
            raise RuntimeError(f"tombol tidak ketemu: {cond_js}")
        self.click(pos[0], pos[1])
        return pos

    def field(self, label: str, value) -> bool:
        loc = _FIELD % json.dumps(label)
        pos = self.t.ev(loc)
        if not pos:
            return False
        self.fill_input(pos[0], pos[1], value, clicks=3, locate=loc)  # panel may still be sliding in
        _nap(0.5)
        return True

    def position_panel(self):
        if not self.t.ev(_FIELD % json.dumps("X")):
            self.button("t==='Position'||t.startsWith('Position panel')")
            self.t.wait(_FIELD % json.dumps("X"), 6)

    def place(self, x, y, w=None, h=None, keep_ratio=True, is_text=False):
        self.assert_single()
        self.position_panel()
        lock = self.t.ev("""(()=>{const f=[...document.querySelectorAll('input')].find(i=>{const l=i.closest('label')||i.parentElement?.parentElement;
            return (l?.innerText||'').trim().startsWith('Height')});if(!f)return null;const fr=f.getBoundingClientRect();
            const b=[...document.querySelectorAll('button')].find(b=>{const r=b.getBoundingClientRect();return Math.abs(r.y-fr.y)<12&&r.x>fr.x+fr.width});
            if(!b)return null;const r=b.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,b.getAttribute('aria-pressed')]})()""")
        if is_text and w is not None:  # text: unlocked width = wrap width (locked would scale the font)
            if lock and lock[2] == "true":
                self.click(lock[0], lock[1])
            self.field("Width", w)
        elif w is not None and h is not None and not keep_ratio:
            if lock and lock[2] == "true":
                self.click(lock[0], lock[1])
            self.field("Width", w); self.field("Height", h)
        elif w is not None:
            if lock and lock[2] == "false":
                self.click(lock[0], lock[1])
            self.field("Width", w)
        self.field("X", x); self.field("Y", y)

    # -- high level ------------------------------------------------------------------------------------------
    def canvas_center(self):
        return self.t.ev("""(()=>{const c=[...document.querySelectorAll('[aria-label="Canvas"],input[aria-label="Canvas"]')][0];
            const r=(c||document.body).getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""") or [800, 450]

    def selected_size(self):
        p = self.t.ev(_FIELD % json.dumps("Width"))
        return p[2] if p else None

    def add_image(self, path, x, y, w=None, h=None):
        before = self.selected_size()
        cx, cy = self.canvas_center()
        data = {"items": [], "files": [str(Path(path).resolve())], "dragOperationsMask": 1}
        for typ in ("dragEnter", "dragOver", "drop"):
            self.t.send("Input.dispatchDragEvent", {"type": typ, "x": cx, "y": cy, "data": data})
            _nap(0.4)
        end = time.time() + 120  # wait until the new image is inserted and selected
        while time.time() < end:
            _nap(2)
            try:
                self.position_panel()
            except RuntimeError:
                continue  # upload still running, nothing selected yet
            now = self.selected_size()
            if now and now != before:
                break
        self.place(x, y, w, h, keep_ratio=h is None)

    def add_text(self, text, font=None, size=None, color=None, x=0, y=0, w=None, bold=False, align="left"):
        """Fast path: copy a box of the same style already on this page and only change words and place
        (skips the font panel, size, colour, bold and align). Falls back to a fresh box on any problem."""
        page = (self.page_counter() or [None])[0]
        if page != self.styled_page:
            self.styled, self.styled_page = {}, page
        key = (font, size, (color or "").upper(), bool(bold), align)
        src = self.styled.get(key)
        if src and _os.getenv("CANVA_STYLE_REUSE", "1") != "0":
            try:
                self._add_text_copy(src, text, x, y, w)
                self.styled[key] = text
                return
            except Exception:
                self.styled.pop(key, None)
                self.key("Escape"); self.key("Escape")
        self._add_text_fresh(text, font, size, color, x, y, w, bold, align)
        self.styled[key] = text

    def _add_text_copy(self, src, text, x, y, w):
        self.select_text(src)
        before = self.t.ev("document.querySelectorAll('p').length")
        self.copy(); _nap(0.4); self.paste()
        if not self.t.wait("document.querySelectorAll('p').length>%d" % before, 5):
            raise RuntimeError("salinan kotak teks tidak muncul")
        _nap(0.6)
        self.assert_single()
        self.key("Enter")
        if not self.t.wait("document.activeElement && document.activeElement.isContentEditable", 4):
            self.key("Delete"); raise RuntimeError("salinan tidak bisa diedit; dihapus")
        self.key("a", ctrl=True); self.type_lines(text); _nap(0.5)
        typed = self.t.ev("document.activeElement && document.activeElement.isContentEditable ? document.activeElement.innerText : null")
        self.key("Escape"); _nap(0.6)
        if _flat(typed) != _flat(text):
            self.assert_single(); self.key("Delete")
            raise RuntimeError("teks salinan tidak cocok; salinan dihapus")
        self.place(x, y, w, is_text=True)
        self.key("Escape")

    def _add_text_fresh(self, text, font=None, size=None, color=None, x=0, y=0, w=None, bold=False, align="left"):
        self.focus_workspace()
        self.key("t")
        if not self.t.wait("document.activeElement && document.activeElement.isContentEditable", 6):
            raise RuntimeError("kotak teks tidak terbuka")
        self.key("a", ctrl=True)  # inside the new box only: the default text
        self.type_lines(text)
        _nap(0.5)
        typed = self.t.ev("document.activeElement && document.activeElement.isContentEditable ? document.activeElement.innerText : null")
        if _flat(typed) != _flat(text):
            # the keystrokes did not land in a fresh text box: revert and stop before anything else is touched
            self.key("Escape"); self.key("z", ctrl=True); self.key("Escape")
            raise RuntimeError(f"teks tidak masuk ke kotak teks baru (terbaca: {typed!r}); dibatalkan")
        self.key("Escape")
        _nap(0.8)
        self.assert_single()
        if not self.text_on_page(text):
            # Canva sometimes drops the first keystrokes right after uploads: edit the box again
            self.key("Enter")
            if self.t.wait("document.activeElement && document.activeElement.isContentEditable", 4):
                self.key("a", ctrl=True); self.type_lines(text); _nap(0.5)
            self.key("Escape"); _nap(0.8)
            self.assert_single()
            if not self.text_on_page(text):
                self.key("Delete")  # the selection is our new box (checked single above)
                raise RuntimeError("teks tidak tersimpan di desain; kotak teks baru dihapus")
        if font:
            self.set_font(font)
        if size:
            self.set_font_size(size)
        self.assert_single()
        if color:
            self.set_text_color(color)
            self.assert_single()
        # always set it: a new text box can start bold (Canva carries the last style over)
        self.set_bold(bool(bold))
        if align:
            self.set_align(align)
        self.place(x, y, w, is_text=True)

    def set_font(self, font):
        """Pick a font for the selected text box from the font panel; one retry with the panel reopened."""
        find = """(()=>{const i=[...document.querySelectorAll('input')].find(i=>i.getBoundingClientRect().x<420&&i.getBoundingClientRect().width>0&&/font|try|search/i.test((i.placeholder||'')+(i.getAttribute('aria-label')||'')));
            if(!i)return null;const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()"""
        pick = "t.split(String.fromCharCode(10))[0].trim()===%s||t.startsWith(%s+',')" % (json.dumps(font), json.dumps(font))
        last = None
        for attempt in range(2):
            try:
                if not self.t.ev(find):  # panel not open yet
                    self.button("t.startsWith('Toggle font selector')")
                    _nap(1.0)  # the font panel slides in
                box = self.t.wait(find, 6)
                if not box:
                    raise RuntimeError("kolom cari font tidak ketemu")
                self.fill_input(box[0], box[1], font, enter=False, locate=find)
                _nap(1.5)
                self.button(pick, wait=10)
                _nap(1)
                return
            except RuntimeError as ex:
                last = ex
                self.assert_single()
                self.button("t.startsWith('Toggle font selector')")  # closes the panel; next try reopens it
                _nap(1.2)
        raise RuntimeError(f"font {font!r}: {last}")

    def type_lines(self, text):
        """Type text; "\\n" becomes Enter (a new paragraph in the same text box), so line breaks are fixed
        and do not depend on Canva's wrapping."""
        for i, line in enumerate(text.split("\n")):
            if i:  # Canva's text editor handles the Enter keydown itself (a char event would add a second break)
                _nap(0.25)
                self.t.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
                self.t.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
                _nap(0.35)
            if line:
                self.type(line)

    def text_on_page(self, text) -> bool:
        """Is `text` rendered in the design (Canva keeps text elements as DOM nodes)? Multi-line text:
        every line must be there."""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return bool(self.t.ev("""(()=>{const want=%s;const norm=s=>(s||'').replace(/[\\ufeff\\u200b-\\u200d]/g,'').replace(/\\u00a0/g,' ').trim();
            const all=[...document.querySelectorAll('p,span,div')].filter(e=>e.children.length<3).map(e=>norm(e.innerText));
            return want.every(w=>all.includes(w))})()""" % json.dumps(lines)))

    def select_text(self, text):
        """Select the existing text box on the active page whose text is `text` (first line is enough) and
        check that exactly that box is selected. Returns its on-screen centre."""
        first = next(l.strip() for l in text.split("\n") if l.strip())
        # Canva collapses runs of spaces; every text also has a hidden copy (inside a 1x1 clip), so only a
        # match that is really under the mouse at its centre counts
        first = " ".join(first.split())
        # only inside the active page (between its "Page n" header and the next one): the same words, e.g. the
        # footer, are on every page and a match on a neighbour page would copy/edit the wrong page
        cur = (self.page_counter() or [0])[0]
        find = """(()=>{const want=%s,cur=%d;const norm=s=>(s||'').replace(/[\\ufeff\\u200b-\\u200d]/g,'').replace(/\\u00a0/g,' ').split('\\n')[0].replace(/\\s+/g,' ').trim();
            const hy=n=>{const h=[...document.querySelectorAll('span,p,div')].find(e=>e.children.length===0&&new RegExp('^Page '+n+'(\\\\s|$)').test((e.innerText||'').trim()));return h?h.getBoundingClientRect().bottom:null};
            const top=hy(cur),nx=hy(cur+1),bot=nx===null?innerHeight:nx-30;if(top===null)return null;
            for(const e of document.querySelectorAll('p,span,div')){if(e.children.length>=3||norm(e.innerText)!==want)continue;
              const r=e.getBoundingClientRect();if(r.width<4||r.y<60||r.bottom>innerHeight-60||r.y<top||r.bottom>bot)continue;
              const x=r.x+r.width/2,y=r.y+r.height/2,h=document.elementFromPoint(x,y);
              if(h&&(e.contains(h)||h.contains(e)))return [x,y]}
            return null})()""" % (json.dumps(first), cur)
        self.focus_workspace()
        p = self.t.ev(find)
        if not p:  # maybe scrolled off: bring the active page fully into view and look again
            self.go_to_page((self.page_counter() or [None])[0]); _nap(1)
            p = self.t.ev(find)
        if not p:
            raise RuntimeError(f"teks {first!r} tidak terlihat di halaman ini")
        self.click(p[0], p[1]); _nap(0.6)
        if self.t.ev("document.activeElement && document.activeElement.isContentEditable"):
            self.key("Escape"); _nap(0.4)
        self.assert_single()
        if not self.t.ev("!!document.querySelector('input[aria-label=\"Font size\"]')"):
            self.key("Escape")
            raise RuntimeError(f"yang terpilih bukan kotak teks {first!r}; tidak diubah")
        return p

    def edit_text(self, old, new):
        """Replace the words of an existing text box; its font, size, colour and place stay as they are."""
        self.select_text(old)
        self.key("Enter")  # into text editing of the selected box
        if not self.t.wait("document.activeElement && document.activeElement.isContentEditable", 4):
            raise RuntimeError("kotak teks tidak bisa diedit")
        self.key("a", ctrl=True); self.type_lines(new); _nap(0.5)
        typed = self.t.ev("document.activeElement && document.activeElement.isContentEditable ? document.activeElement.innerText : null")
        self.key("Escape"); _nap(0.6)
        if _flat(typed) != _flat(new):
            self.key("z", ctrl=True); self.key("Escape")
            raise RuntimeError(f"teks baru tidak masuk (terbaca: {typed!r}); dibatalkan")
        self.key("Escape")

    def delete_text(self, text):
        """Delete one existing text box (only that box: a multi-selection or a non-text element is refused)."""
        self.select_text(text)
        self.key("Delete"); _nap(0.8)

    def move_text(self, text, x, y, w=None):
        """Move (and optionally widen) an existing text box to page coordinates."""
        self.select_text(text)
        self.place(x, y, w, is_text=True)
        self.key("Escape")

    DEFAULT_TEXTS = ("Your paragraph text", "Add a heading", "Add a subheading", "Add a little bit of body text")

    def remove_default_texts(self) -> int:
        """Delete text boxes still holding Canva's placeholder text (left behind when typing did not land)."""
        find = """(()=>{const want=%s;const norm=s=>(s||'').replace(/[\\ufeff\\u200b-\\u200d]/g,'').replace(/\\u00a0/g,' ').trim();
            const e=[...document.querySelectorAll('p,span,div')].find(e=>e.children.length<3&&want.includes(norm(e.innerText))&&e.getBoundingClientRect().width>0);
            if(!e)return null;const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""" % json.dumps(list(self.DEFAULT_TEXTS))
        removed = 0
        for _ in range(6):
            self.focus_workspace()
            p = self.t.ev(find)
            if not p:
                break
            self.click(p[0], p[1]); _nap(0.6)
            if self.t.ev("document.activeElement && document.activeElement.isContentEditable"):
                self.key("Escape"); _nap(0.4)  # leave text editing, keep the box selected
            self.assert_single()
            # only delete when the selection is really a text box (text toolbar shows the font size field);
            # clicking may hit the background image under the placeholder, which must never be deleted
            if not self.t.ev("!!document.querySelector('input[aria-label=\"Font size\"]')"):
                self.key("Escape")
                raise RuntimeError("teks bawaan tidak bisa dipilih tanpa memilih elemen lain; tidak dihapus")
            self.key("Delete"); _nap(0.8)
            removed += 1
        if self.t.ev(find):
            raise RuntimeError("teks bawaan Canva masih tersisa di desain")
        return removed

    def focus_workspace(self):
        """Deselect everything and give the editor keyboard focus by clicking the empty grey gap
        between the page and the "Add page" bar."""
        self.key("Escape"); self.key("Escape")
        p = self.t.ev("""(()=>{const b=[...document.querySelectorAll('button')].find(b=>/Add page/.test(b.innerText||''));
            if(!b)return null;const r=b.getBoundingClientRect();return [r.x+r.width/2,r.y-10]})()""")
        if p:
            self.click(p[0], p[1]); _nap(0.4)
        self.key("Escape")

    def assert_single(self):
        """Refuse to restyle/move when several elements are selected (Canva then offers "Group")."""
        if self.t.ev("[...document.querySelectorAll('button')].some(b=>(b.innerText||'').trim()==='Group'&&b.getBoundingClientRect().width>0)"):
            self.key("Escape")
            raise RuntimeError("lebih dari satu elemen terpilih; dibatalkan agar elemen lain tidak berubah")

    def set_font_size(self, size):
        """Type the size into the toolbar field and read it back; Canva sometimes ignores the first entry."""
        find = """(()=>{const i=document.querySelector('input[aria-label="Font size"]');if(!i)return null;
            const r=i.getBoundingClientRect();return r.width?[r.x+r.width/2,r.y+r.height/2,i.value]:null})()"""
        want = float(size)
        for _ in range(3):
            p = self.t.wait(find, 5)
            if not p:
                raise RuntimeError("kolom ukuran font tidak ketemu")
            try:
                if abs(float(str(p[2]).replace(",", ".")) - want) < 0.05:
                    return
            except ValueError:
                pass
            self.fill_input(p[0], p[1], ("%g" % want), clicks=3, locate=find)
            _nap(0.9)
            self.assert_single()
        p = self.t.ev(find)
        raise RuntimeError(f"ukuran font tidak berubah ke {size} (terbaca {p and p[2]})")

    def set_bold(self, on=True):
        st = self.t.ev(_BTN % "t==='Bold'")
        if st and (st[2] == "true") != on:
            self.click(st[0], st[1]); _nap(0.5)

    def set_align(self, target="left"):
        """The toolbar button cycles left > center > right > justify; its label names the current one."""
        q = "t.startsWith('Toggle text alignment')"
        for _ in range(5):
            lab = self.t.ev("""(()=>{const b=[...document.querySelectorAll('button')].find(b=>(b.getAttribute('aria-label')||'').startsWith('Toggle text alignment'));
                return b?b.getAttribute('aria-label'):null})()""")
            if not lab or lab.lower().endswith(target):
                return
            self.button(q); _nap(0.5)

    def set_text_color(self, hex_color):
        self.button("t.startsWith('Current text color')||t==='Text color'")
        _nap(1.2)
        # "+" / "Add a new color" opens the picker with a hex input
        self.button("/new colou?r|add a new colou?r/i.test(t)", wait=6)
        inp = self.t.wait("""(()=>{const i=[...document.querySelectorAll('input')].find(i=>/^#?[0-9a-f]{6}$/i.test(i.value||'')||/hex/i.test(i.getAttribute('aria-label')||''));
            if(!i)return null;const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""", 6)
        if not inp:
            raise RuntimeError("input hex warna tidak ketemu")
        self.fill_input(inp[0], inp[1], hex_color.lstrip("#"), clicks=3)
        _nap(0.8)
        self.key("Escape")

    # only the editor footer: a slide can itself contain text like "1 / 11"
    PAGE_COUNTER = """(()=>{const e=[...document.querySelectorAll('span,div,p,button')].filter(e=>e.children.length<2&&/^\\d+ \\/ \\d+$/.test((e.innerText||'').trim())
        &&!e.closest('[contenteditable],p')&&e.getBoundingClientRect().y>innerHeight-90&&e.getBoundingClientRect().width>0
        &&e.getBoundingClientRect().x>innerWidth-260&&!/^0/.test(e.innerText.trim())).pop();  // not a "07 / 16" printed on a slide
        return e?e.innerText.trim().split(' / ').map(Number):null})()"""

    def page_counter(self):
        """[current page, page count] from the editor footer, e.g. [2, 2]."""
        return self.t.ev(self.PAGE_COUNTER)

    def add_page(self):
        """Append an empty page with the "+ Add page" bar under the last page; the new page becomes active."""
        self.key("Escape"); self.key("Escape")
        before = self.page_counter() or [0, 0]
        if before[0] != before[1]:  # Canva inserts after the active page: start from the last one
            self.go_to_page(before[1]); before = self.page_counter() or before
        # the active page's header icon (aria-label "Add page") is on screen; the bar under the last page
        # may be scrolled out of view
        self.button("b.getAttribute('aria-label')==='Add page'&&!(b.innerText||'').trim()"
                    "&&b.getBoundingClientRect().y>60&&b.getBoundingClientRect().bottom<innerHeight-60")
        # Canva inserts the page after the active one and makes it active
        if not self.t.wait("(()=>{const c=%s;return c&&c[1]===%d})()" % (self.PAGE_COUNTER.strip(), before[1] + 1), 15):
            raise RuntimeError(f"halaman baru tidak muncul (sebelumnya {before}, sekarang {self.page_counter()})")
        _nap(1.5)
        # the counter can lag behind the new page for a moment: wait for it rather than a fixed pause
        self.t.wait("(()=>{const c=%s;return c&&c[0]===c[1]})()" % self.PAGE_COUNTER.strip(), 8)
        now = self.page_counter() or [None, None]
        if now[0] != now[1]:
            raise RuntimeError(f"halaman baru bukan halaman terakhir ({now})")
        return now[0]

    def go_to_page(self, n=None):
        """Make page n (default: the last page) the active page: scroll the page list and click its "Page n" header."""
        self.key("Escape"); self.key("Escape")
        total = (self.page_counter() or [1, 1])[1]
        n = total if n is None else n
        if n == total:  # last page: jump straight to the bottom of the page list
            self.t.ev("""(()=>{const s=[...document.querySelectorAll('div')].find(d=>d.scrollHeight>d.clientHeight+200&&/auto|scroll/.test(getComputedStyle(d).overflowY)&&d.clientWidth>600);
                if(s)s.scrollTop=s.scrollHeight})()""")
            _nap(1.5)
        for step in range(45):
            if (self.page_counter() or [None])[0] == n:
                return n
            if step == 30:  # stuck (seen near pages 30-31): restart the search from the bottom of the list
                self.t.ev("""(()=>{const s=[...document.querySelectorAll('div')].find(d=>d.scrollHeight>d.clientHeight+200&&/auto|scroll/.test(getComputedStyle(d).overflowY)&&d.clientWidth>600);
                    if(s)s.scrollTop=s.scrollHeight})()""")
                _nap(1.5)
            p = self.t.ev("""(()=>{const h=[...document.querySelectorAll('span,p,div')].find(e=>e.children.length===0&&
                new RegExp('^Page %d(\\\\s|$)').test((e.innerText||'').trim()));
              const s=[...document.querySelectorAll('div')].find(d=>d.scrollHeight>d.clientHeight+200&&/auto|scroll/.test(getComputedStyle(d).overflowY)&&d.clientWidth>600);
              if(h){const r=h.getBoundingClientRect();if(r.y>70&&r.bottom<innerHeight-70)return [r.x+r.width/2,r.y+r.height/2];
                if(s)s.scrollTop+=r.y-innerHeight/3;return null}
              if(s){const hs=[...document.querySelectorAll('span,p,div')].filter(e=>e.children.length===0&&/^Page \\d+(\\s|$)/.test((e.innerText||'').trim()));
                const first=hs.length?+hs[0].innerText.match(/\\d+/)[0]:1;s.scrollTop+=(%d>first?1:-1)*s.clientHeight*0.8}
              return null})()""" % (n, n))
            if p:
                self.click(p[0], p[1])
            _nap(1.2)
        if (self.page_counter() or [None])[0] != n:
            raise RuntimeError(f"tidak bisa pindah ke halaman {n} (sekarang {self.page_counter()})")
        return n

    def set_title(self, title):
        p = self.t.ev("""(()=>{const i=document.querySelector('input[aria-label="Design title"]');if(!i)return null;
            const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""")
        if p:
            self.fill_input(p[0], p[1], title)


def _find_tab(pred) -> dict | None:
    for t in json.load(urllib.request.urlopen(BASE + "/json", timeout=5)):
        if t.get("type") == "page" and pred(t):
            return t
    return None


def create_design(width: int, height: int) -> str:
    """Home > Create a design > Custom size. Returns the editor URL of the new design."""
    home = _Tab("https://www.canva.com/")
    try:
        ed = Editor(home)
        boxes_js = """(()=>{const n=[...document.querySelectorAll('input[type=number]')].filter(i=>i.getBoundingClientRect().width>0);
            return n.length>=2?n.slice(0,2).map(i=>{const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}):null})()"""
        boxes = None
        tabs_before = {t["id"] for t in json.load(urllib.request.urlopen(BASE + "/json", timeout=5))}
        for _ in range(4):  # the home page may still be hydrating: retry until the size dialog shows
            # Never click the "Quick Create" carousel: it shifts while loading and a click can land on
            # "Email" or "Presentation" and open an unwanted design. Use the "Create a design" dialog's
            # side menu, whose entries do not move.
            # Canva's home changes often: find any visible element whose text is exactly "Custom size"
            # (a menu row, a tile label...) and click it once it stops moving.
            find = """(()=>{const c=[...document.querySelectorAll('button,a,[role=button],[role=menuitem],[role=option],div,span,p')]
                .filter(e=>e.children.length<4&&(e.innerText||'').trim()==='Custom size').map(e=>e.getBoundingClientRect())
                .filter(r=>r.width>30&&r.height>10&&r.y>0&&r.y<innerHeight);
                const r=c[c.length-1];return r?[r.x+r.width/2,r.y+r.height/2]:null})()"""
            end, last, pos = time.time() + 40, None, None
            while time.time() < end:
                p = home.ev(find)
                if p and last and abs(p[0] - last[0]) < 1 and abs(p[1] - last[1]) < 1:
                    pos = p
                    break
                last = p
                _nap(0.8)
            if pos:
                ed.click(pos[0], pos[1])
            boxes = home.wait(boxes_js, 8)
            if not boxes and pos is None:
                ed.stable_button("t==='Create a design'", wait=20)  # older layout: open the dialog first
                _nap(2)
                continue
            if boxes:
                break
            ed.key("Escape"); time.sleep(3)
            for t in json.load(urllib.request.urlopen(BASE + "/json", timeout=5)):  # stray design tab? close it
                if t["id"] not in tabs_before and t.get("type") == "page":
                    urllib.request.urlopen(f"{BASE}/json/close/{t['id']}", timeout=5)
        if not boxes:
            raise RuntimeError("dialog Custom size tidak muncul")
        for (bx, by), v in zip(boxes, (width, height)):
            ed.fill_input(bx, by, v, clicks=3, enter=False)
        _nap(1)
        before = {t["id"] for t in json.load(urllib.request.urlopen(BASE + "/json", timeout=5))}
        # the button stays disabled until Canva has taken both numbers; clicking earlier does nothing
        home.wait("(()=>{const b=[...document.querySelectorAll('button')].find(b=>(b.innerText||'').trim()==='Create new design');"
                  "return b&&!b.disabled&&b.getAttribute('aria-disabled')!=='true'})()", 10)
        ed.button("t==='Create new design'")
        end = time.time() + 90
        while time.time() < end:
            _nap(2)
            # wait for the real id: the first URL is a transient ".../design/editor/shell?create..." one
            t = _find_tab(lambda t: t["id"] not in before and re.search(r"/design/D[\w-]+/", t.get("url", "")))
            if t:
                return t["url"]
        raise RuntimeError("desain baru tidak terbuka")
    finally:
        home.close()


def _open_editor(url: str, tries: int = 4) -> _Tab:
    """Open the editor in a fresh tab; a tab that stops answering while loading is closed and reopened."""
    import websocket
    last = None
    for _ in range(tries):
        tab = _Tab(url)
        try:
            if tab.wait("!!document.querySelector('input[aria-label=\"Design title\"]')", 60):
                time.sleep(3)
                tab.ev("1")  # still responsive after load?
                return tab
            last = "editor tidak selesai dimuat"
        except (websocket.WebSocketTimeoutException, TimeoutError) as ex:
            last = repr(ex)
        tab.close()
        time.sleep(10)
    raise RuntimeError(f"editor Canva tidak merespons ({url}): {last}")


def shortcut_selftest(design_url: str | None = None) -> dict:
    """Check the keyboard shortcuts against the live editor by counting copies of a marker text box."""
    st = ensure_chrome()
    if not st.get("running"):
        return {"ok": False, **st}
    url = design_url or create_design(800, 600)
    if not design_url:
        time.sleep(12)
    tab = _open_editor(url)
    ed = Editor(tab)
    mark = "KEYTEST-%d" % (int(time.time()) % 100000)
    count_js = """[...document.querySelectorAll('p')].filter(p=>p.innerText.trim()===%s&&p.getBoundingClientRect().width>0
        &&getComputedStyle(p).fontFamily.indexOf('Times')<0).length""" % json.dumps(mark)
    multi_js = "[...document.querySelectorAll('button')].some(b=>(b.innerText||'').trim()==='Group'&&b.getBoundingClientRect().width>0)"
    steps = []

    def n():
        _nap(1.5)
        return tab.ev(count_js)

    def check(name, combo, expect, got, extra=None):
        steps.append({"step": name, "keys": combo, "expect": expect, "got": got, "ok": expect == got, **(extra or {})})

    try:
        ed.add_text(mark, size=40, x=60, y=60)
        base = n()
        check("tambah teks", "-", 1, base)
        ed.copy(); ed.paste()
        check("salin + tempel", "ctrl+c, ctrl+v", 2, n())
        ed.undo()
        check("undo", "ctrl+z", 1, n())
        ed.redo()
        check("redo", "ctrl+y", 2, n())
        ed.undo(); n(); ed.hotkey("ctrl+shift+z")
        check("redo (alternatif)", "ctrl+shift+z", 2, n())
        ed.focus_workspace(); ed.select_all(); _nap(1)
        check("pilih semua", "ctrl+a", True, bool(tab.ev(multi_js)))
        ed.cut()
        check("potong", "ctrl+x", 0, n())
        ed.paste()
        check("tempel hasil potong", "ctrl+v", 2, n())
        ed.focus_workspace(); ed.select_all(); _nap(0.8)
        ed.hotkey("shift+ctrl+x")  # Canva has no cut on Shift+Ctrl+X: the elements must stay
        check("shift+ctrl+x (Canva tidak memotong, elemen tetap)", "shift+ctrl+x", 2, n())
        ed.focus_workspace(); ed.select_all(); _nap(0.8)
        ed.duplicate()
        check("duplikat", "ctrl+d", 4, n())
        ed.focus_workspace(); ed.select_all(); _nap(0.8)
        ed.hotkey("Delete")
        check("hapus", "Delete", 0, n())
        ed.undo()
        check("undo hapus", "ctrl+z", 4, n())
        # every combo must reach the page as the right keydown (modifiers included); typed into a scratch
        # textarea so nothing in the design is touched
        combos = ["ctrl+z", "ctrl+y", "ctrl+shift+z", "ctrl+c", "ctrl+v", "ctrl+x", "ctrl+a", "shift+ctrl+x",
                  "ctrl+d", "ctrl+g", "ctrl+shift+g", "ctrl+b", "ctrl+i", "ctrl+u", "ctrl+s", "ctrl+=", "ctrl+-",
                  "alt+shift+t", "shift+ArrowUp", "Delete", "Backspace", "Escape", "Enter", "F2", "Tab"]
        ed.key("Escape"); ed.key("Escape")
        tab.ev("""(()=>{window.__keylog=[];const ta=document.createElement('textarea');ta.id='__keytest';
            ta.style.cssText='position:fixed;left:0;top:0;width:20px;height:20px;opacity:0.01;z-index:99999';document.body.appendChild(ta);
            ta.addEventListener('keydown',e=>{if(!/^(Control|Shift|Alt|Meta)$/.test(e.key))window.__keylog.push([e.key,e.code,e.ctrlKey,e.shiftKey,e.altKey]);e.preventDefault();e.stopPropagation()},true);
            ta.focus();return document.activeElement===ta})()""")
        for c in combos:
            ed.hotkey(c)
        log = tab.ev("window.__keylog") or []
        tab.ev("document.getElementById('__keytest')?.remove()")
        for c, got in zip(combos, log + [None] * (len(combos) - len(log))):
            mods = {m.lower() for m in c.split("+")[:-1]}
            want = [("ctrl" in mods), ("shift" in mods), ("alt" in mods)]
            check(f"keydown {c}", c, True, bool(got) and got[2:5] == want, {"event": got})
        shot =tab.screenshot(Path.home() / ".creative-mcp" / "canva_shortcut_selftest.png")
        return {"ok": all(s["ok"] for s in steps), "design_url": tab.ev("location.href"), "steps": steps, "screenshot": shot}
    finally:
        tab.ws.close()


def edit(design_url: str, ops: list[dict]) -> dict:
    """Change an existing design in place, without rebuilding pages. Each op:
    {"page": n, "action": "replace", "text": old, "new": new} | {"page": n, "action": "delete", "text": t}
    | {"page": n, "action": "move", "text": t, "x": .., "y": .., "w": ..} | {"page": n, "action": "add", ...text element}.
    Text is found by its first line on that page; anything ambiguous is refused, never guessed."""
    st = ensure_chrome()
    if not st.get("running"):
        return {"ok": False, **st}
    existing = _find_tab(lambda t: t.get("url", "").split("?")[0] == design_url.split("?")[0])
    if existing:
        urllib.request.urlopen(f"{BASE}/json/close/{existing['id']}", timeout=5)
    tab = _open_editor(design_url)
    ed = Editor(tab)
    done, errors = [], []
    try:
        for i, op in enumerate(ops):
            try:
                ed.go_to_page(int(op["page"])); _nap(1)
                a = op.get("action", "replace")
                if a == "replace":
                    ed.edit_text(op["text"], op["new"])
                    if not ed.text_on_page(op["new"]):
                        raise RuntimeError("teks baru tidak terbaca di halaman")
                elif a == "delete":
                    ed.delete_text(op["text"])
                elif a == "move":
                    ed.move_text(op["text"], op["x"], op["y"], op.get("w"))
                elif a == "add":
                    ed.add_text(op["text"], op.get("font"), op.get("size"), op.get("color"), op.get("x", 0), op.get("y", 0),
                                op.get("w"), op.get("bold", False), op.get("align", "left"))
                else:
                    raise ValueError(f"aksi tidak dikenal: {a}")
                done.append(i)
            except Exception as ex:  # one bad op must not touch or stop the others
                errors.append({"op": i, "error": str(ex)})
                ed.key("Escape"); ed.key("Escape")
        shot = tab.screenshot(Path.home() / ".creative-mcp" / "canva_edit_last.png")
        return {"ok": not errors, "design_url": design_url, "done": done, "errors": errors, "screenshot": shot}
    finally:
        tab.ws.close()


def build(spec: dict) -> dict:
    import websocket
    """Create (or open) a design and add the spec's elements as native Canva elements."""
    st = ensure_chrome()
    if not st.get("running"):
        return {"ok": False, **st}
    url = spec.get("design_url") or create_design(int(spec["width"]), int(spec["height"]))
    existing = _find_tab(lambda t: t.get("url", "").split("?")[0] == url.split("?")[0])
    if existing:  # close it and reopen fresh: old tabs may stop answering
        urllib.request.urlopen(f"{BASE}/json/close/{existing['id']}", timeout=5)
    if not spec.get("design_url"):
        time.sleep(12)  # a brand-new design is still being saved; reopening it at once tends to hang
    tab = _open_editor(url)
    ed = Editor(tab)
    # "pages": [{"elements": [...]}, ...] builds a multi-page design (slides). A plain "elements" list is one page.
    # A new design fills its blank first page; with design_url the pages are appended after the existing ones
    # (set "fill_current_page": true to put the first spec page on the page that is open).
    pages = spec.get("pages") or [{"elements": spec.get("elements", [])}]
    fill_first = not spec.get("design_url") or spec.get("fill_current_page", False)
    log = Path.home() / ".creative-mcp" / "canva_native_progress.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)

    def note(**kw):
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"t": time.strftime("%H:%M:%S"), **kw}, ensure_ascii=False) + "\n")

    done, errors, removed, page_numbers = [], [], 0, []
    try:
        if spec.get("title"):
            ed.set_title(spec["title"])
        if spec.get("design_url"):
            # the editor opens on whatever page was viewed last; resume work always happens at the end
            ed.go_to_page()
        if fill_first and spec.get("clear_current_page"):
            ed.focus_workspace(); ed.select_all(); _nap(1); ed.hotkey("Delete"); _nap(1.5)
        reopen_every = int(spec.get("reopen_every", 4))
        for pi, page in enumerate(pages):
            if pi and reopen_every and pi % reopen_every == 0:
                # a Canva tab slows down and eventually stops answering after many large uploads: start fresh
                tab.close(); time.sleep(3)
                tab = _open_editor(url); ed = Editor(tab); ed.go_to_page()
            if pi or not fill_first:
                ed.add_page()
            tab.wake()
            page_numbers.append((ed.page_counter() or [None])[0])
            note(page=pi, canva_page=page_numbers[-1], start=True)
            els = page.get("elements", [])
            ok_here = []
            for i, e in enumerate(els):
                for attempt in range(2):
                    try:
                        # never put an element on another page (a reconnect or scroll can move the active page)
                        cur = ed.page_counter()
                        if page_numbers[-1] and cur and cur[0] != page_numbers[-1]:
                            ed.go_to_page(page_numbers[-1])
                        if e["type"] == "image":
                            ed.add_image(e["path"], e.get("x", 0), e.get("y", 0), e.get("w"), e.get("h"))
                        elif e["type"] == "text":
                            ed.add_text(e["text"], e.get("font"), e.get("size"), e.get("color"), e.get("x", 0), e.get("y", 0), e.get("w"), e.get("bold", False), e.get("align", "left"))
                        ok_here.append(i); pace_ok()
                        note(page=pi, element=i, ok=True, pace=round(_pace[0], 2))
                        break
                    except (websocket.WebSocketTimeoutException, TimeoutError, ConnectionError) as ex:
                        # the tab froze (e.g. another tab came to the front): reconnect, wake it, retry once
                        pace_fail(); note(page=pi, element=i, ok=False, error=f"tab beku, sambung ulang: {ex}")
                        try:
                            tab.reconnect(); time.sleep(3)
                        except Exception:  # dead for good: reopen the editor on the page being built (the last one)
                            tab.close(); time.sleep(5)
                            tab = _open_editor(url); ed = Editor(tab); ed.go_to_page()
                        if attempt:
                            errors.append({"page": pi, "element": i, "error": str(ex)})
                    except Exception as ex:  # keep going: one failed element should not lose the rest
                        pace_fail(); errors.append({"page": pi, "element": i, "error": str(ex)})
                        note(page=pi, element=i, ok=False, error=str(ex))
                        break
            ed.key("Escape"); ed.key("Escape")
            try:  # never report success while a placeholder box sits on the page
                removed += ed.remove_default_texts()
            except Exception as ex:
                errors.append({"page": pi, "element": None, "error": f"pembersihan teks bawaan: {ex}"})
            # check this page now: Canva drops off-screen pages from the DOM
            for i in list(ok_here):
                if els[i]["type"] == "text" and not ed.text_on_page(els[i]["text"]):
                    ok_here.remove(i)
                    errors.append({"page": pi, "element": i, "error": "teks tidak ada di desain setelah build"})
            done.extend((pi, i) for i in ok_here)
            if spec.get("page_shots"):
                tab.screenshot(Path(spec["page_shots"]) / f"page{pi + 1:02d}.png")
        time.sleep(3)
        shot = tab.screenshot(Path.home() / ".creative-mcp" / "canva_native_last.png")
        added = [i for _, i in done] if len(pages) == 1 else [list(d) for d in done]
        return {"ok": not errors, "design_url": tab.ev("location.href"), "pages": len(pages), "canva_pages": page_numbers,
                "added": added, "errors": errors, "default_text_removed": removed, "screenshot": shot}
    finally:
        tab.ws.close()  # leave the editor tab open for the user
