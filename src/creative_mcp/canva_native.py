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

_FIELD = """(()=>{const i=[...document.querySelectorAll('input')].find(i=>{const l=i.closest('label')||i.parentElement?.parentElement;
  return (l?.innerText||'').trim().split(String.fromCharCode(10))[0]===%s});if(!i)return null;
  const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,i.value]})()"""
_BTN = """(()=>{const b=[...document.querySelectorAll('button,[role=button],[role=option],[role=tab]')].find(b=>{
  const t=(b.getAttribute('aria-label')||b.innerText||'').trim();return %s});if(!b)return null;
  const r=b.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,b.getAttribute('aria-pressed')]})()"""


class Editor:
    def __init__(self, tab: _Tab):
        self.t = tab

    # -- low level -------------------------------------------------------------------------------------------
    def click(self, x, y, n=1, button="left"):
        s = self.t.send
        s("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        for i in range(1, n + 1):
            s("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": button, "clickCount": i})
            s("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": button, "clickCount": i})

    def key(self, k, ctrl=False, shift=False):
        code = {"Enter": 13, "Escape": 27, "Delete": 46}.get(k) or ord(k.upper())
        base = {"key": k, "code": k if len(k) > 1 else "Key" + k.upper(), "windowsVirtualKeyCode": code, "modifiers": (2 if ctrl else 0) | (8 if shift else 0)}
        self.t.send("Input.dispatchKeyEvent", {"type": "rawKeyDown", **base})
        if len(k) == 1 and not ctrl and not shift:
            self.t.send("Input.dispatchKeyEvent", {"type": "char", "text": k, **base})
        self.t.send("Input.dispatchKeyEvent", {"type": "keyUp", **base})

    def type(self, text):
        self.t.send("Input.insertText", {"text": text})

    def fill_input(self, x, y, value, clicks=1, enter=True, locate=None):
        """Click an <input>, then replace its value. Never sends Ctrl+A: if the click missed the input,
        Ctrl+A would select every element on the page and the next edits would hit all of them.
        `locate` (JS returning [x, y]) re-measures the input between attempts, e.g. while a panel slides in."""
        for attempt in range(3):
            if locate and attempt:
                time.sleep(0.8)
                p = self.t.ev(locate)
                if p:
                    x, y = p[0], p[1]
            self.click(x, y, clicks)
            time.sleep(0.25)
            if self.t.ev("""(()=>{const a=document.activeElement;if(!a||!/^(INPUT|TEXTAREA)$/.test(a.tagName))return false;
                a.select();return true})()"""):
                self.type(str(value))
                if enter:
                    self.key("Enter")
                return
            if not locate:
                time.sleep(0.6)
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
        pos = self.t.ev(_FIELD % json.dumps(label))
        if not pos:
            return False
        self.fill_input(pos[0], pos[1], value, clicks=3)
        time.sleep(0.5)
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
            time.sleep(0.4)
        end = time.time() + 60  # wait until the new image is inserted and selected
        while time.time() < end:
            time.sleep(2)
            self.position_panel()
            now = self.selected_size()
            if now and now != before:
                break
        self.place(x, y, w, h, keep_ratio=h is None)

    def add_text(self, text, font=None, size=None, color=None, x=0, y=0, w=None, bold=False, align="left"):
        self.focus_workspace()
        self.key("t")
        if not self.t.wait("document.activeElement && document.activeElement.isContentEditable", 6):
            raise RuntimeError("kotak teks tidak terbuka")
        self.key("a", ctrl=True)  # inside the new box only: the default text
        self.type(text)
        time.sleep(0.5)
        typed = self.t.ev("document.activeElement && document.activeElement.isContentEditable ? document.activeElement.innerText : null")
        clean = re.sub(r"[﻿​‌‍]", "", typed or "").replace(" ", " ").strip()
        if clean != text.strip():
            # the keystrokes did not land in a fresh text box: revert and stop before anything else is touched
            self.key("Escape"); self.key("z", ctrl=True); self.key("Escape")
            raise RuntimeError(f"teks tidak masuk ke kotak teks baru (terbaca: {typed!r}); dibatalkan")
        self.key("Escape")
        time.sleep(0.8)
        self.assert_single()
        if not self.text_on_page(text):
            # Canva sometimes drops the first keystrokes right after uploads: edit the box again
            self.key("Enter")
            if self.t.wait("document.activeElement && document.activeElement.isContentEditable", 4):
                self.key("a", ctrl=True); self.type(text); time.sleep(0.5)
            self.key("Escape"); time.sleep(0.8)
            self.assert_single()
            if not self.text_on_page(text):
                self.key("Delete")  # the selection is our new box (checked single above)
                raise RuntimeError("teks tidak tersimpan di desain; kotak teks baru dihapus")
        if font:
            self.button("t.startsWith('Toggle font selector')")
            find = """(()=>{const i=[...document.querySelectorAll('input')].find(i=>i.getBoundingClientRect().x<420&&i.getBoundingClientRect().width>0&&/font|try|search/i.test((i.placeholder||'')+(i.getAttribute('aria-label')||'')));
                if(!i)return null;const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()"""
            time.sleep(1.0)  # the font panel slides in
            box = self.t.wait(find, 6)
            if not box:
                raise RuntimeError("kolom cari font tidak ketemu")
            self.fill_input(box[0], box[1], font, enter=False, locate=find)
            time.sleep(1.5)
            self.button("t.split(String.fromCharCode(10))[0].trim()===%s||t.startsWith(%s+',')" % (json.dumps(font), json.dumps(font)), wait=10)
            time.sleep(1)
        if size:
            self.set_font_size(size)
        self.assert_single()
        if color:
            self.set_text_color(color)
            self.assert_single()
        if bold:
            self.set_bold(True)
        if align:
            self.set_align(align)
        self.place(x, y, w, is_text=True)

    def text_on_page(self, text) -> bool:
        """Is `text` rendered in the design (Canva keeps text elements as DOM nodes)?"""
        return bool(self.t.ev("""(()=>{const want=%s;const norm=s=>(s||'').replace(/[\ufeff\u200b-\u200d]/g,'').replace(/\u00a0/g,' ').trim();
            return [...document.querySelectorAll('p,span,div')].some(e=>e.children.length<3&&norm(e.innerText)===want)})()""" % json.dumps(text.strip())))

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
            self.click(p[0], p[1]); time.sleep(0.6)
            if self.t.ev("document.activeElement && document.activeElement.isContentEditable"):
                self.key("Escape"); time.sleep(0.4)  # leave text editing, keep the box selected
            self.assert_single()
            # only delete when the selection is really a text box (text toolbar shows the font size field);
            # clicking may hit the background image under the placeholder, which must never be deleted
            if not self.t.ev("!!document.querySelector('input[aria-label=\"Font size\"]')"):
                self.key("Escape")
                raise RuntimeError("teks bawaan tidak bisa dipilih tanpa memilih elemen lain; tidak dihapus")
            self.key("Delete"); time.sleep(0.8)
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
            self.click(p[0], p[1]); time.sleep(0.4)
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
            time.sleep(0.9)
            self.assert_single()
        p = self.t.ev(find)
        raise RuntimeError(f"ukuran font tidak berubah ke {size} (terbaca {p and p[2]})")

    def set_bold(self, on=True):
        st = self.t.ev(_BTN % "t==='Bold'")
        if st and (st[2] == "true") != on:
            self.click(st[0], st[1]); time.sleep(0.5)

    def set_align(self, target="left"):
        """The toolbar button cycles left > center > right > justify; its label names the current one."""
        q = "t.startsWith('Toggle text alignment')"
        for _ in range(5):
            lab = self.t.ev("""(()=>{const b=[...document.querySelectorAll('button')].find(b=>(b.getAttribute('aria-label')||'').startsWith('Toggle text alignment'));
                return b?b.getAttribute('aria-label'):null})()""")
            if not lab or lab.lower().endswith(target):
                return
            self.button(q); time.sleep(0.5)

    def set_text_color(self, hex_color):
        self.button("t.startsWith('Current text color')||t==='Text color'")
        time.sleep(1.2)
        # "+" / "Add a new color" opens the picker with a hex input
        self.button("/new colou?r|add a new colou?r/i.test(t)", wait=6)
        inp = self.t.wait("""(()=>{const i=[...document.querySelectorAll('input')].find(i=>/^#?[0-9a-f]{6}$/i.test(i.value||'')||/hex/i.test(i.getAttribute('aria-label')||''));
            if(!i)return null;const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""", 6)
        if not inp:
            raise RuntimeError("input hex warna tidak ketemu")
        self.fill_input(inp[0], inp[1], hex_color.lstrip("#"), clicks=3)
        time.sleep(0.8)
        self.key("Escape")

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
        for _ in range(4):  # the home page may still be hydrating: retry until the size dialog shows
            ed.button("/^Custom size/.test(t)", wait=40)
            boxes = home.wait(boxes_js, 8)
            if boxes:
                break
            ed.key("Escape"); time.sleep(3)
        if not boxes:
            raise RuntimeError("dialog Custom size tidak muncul")
        for (bx, by), v in zip(boxes, (width, height)):
            ed.fill_input(bx, by, v, clicks=3, enter=False)
        time.sleep(1)
        before = {t["id"] for t in json.load(urllib.request.urlopen(BASE + "/json", timeout=5))}
        ed.button("t==='Create new design'")
        end = time.time() + 90
        while time.time() < end:
            time.sleep(2)
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


def build(spec: dict) -> dict:
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
    done, errors = [], []
    try:
        if spec.get("title"):
            ed.set_title(spec["title"])
        for i, e in enumerate(spec.get("elements", [])):
            try:
                if e["type"] == "image":
                    ed.add_image(e["path"], e.get("x", 0), e.get("y", 0), e.get("w"), e.get("h"))
                elif e["type"] == "text":
                    ed.add_text(e["text"], e.get("font"), e.get("size"), e.get("color"), e.get("x", 0), e.get("y", 0), e.get("w"), e.get("bold", False), e.get("align", "left"))
                done.append(i)
            except Exception as ex:  # keep going: one failed element should not lose the rest
                errors.append({"element": i, "error": str(ex)})
        ed.key("Escape"); ed.key("Escape")
        removed = 0
        try:  # never report success while a placeholder box sits on the page
            removed = ed.remove_default_texts()
        except Exception as ex:
            errors.append({"element": None, "error": f"pembersihan teks bawaan: {ex}"})
        missing = [i for i in done if spec["elements"][i]["type"] == "text" and not ed.text_on_page(spec["elements"][i]["text"])]
        for i in missing:
            done.remove(i)
            errors.append({"element": i, "error": "teks tidak ada di desain setelah build"})
        time.sleep(3)
        shot = tab.screenshot(Path.home() / ".creative-mcp" / "canva_native_last.png")
        return {"ok": not errors, "design_url": tab.ev("location.href"), "added": done, "errors": errors,
                "default_text_removed": removed, "screenshot": shot}
    finally:
        tab.ws.close()  # leave the editor tab open for the user
