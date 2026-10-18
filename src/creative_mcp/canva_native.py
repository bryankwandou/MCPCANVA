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
        self.click(pos[0], pos[1], 3)
        self.key("a", ctrl=True)
        self.type(str(value))
        self.key("Enter")
        time.sleep(0.5)
        return True

    def position_panel(self):
        if not self.t.ev(_FIELD % json.dumps("X")):
            self.button("t==='Position'||t.startsWith('Position panel')")
            self.t.wait(_FIELD % json.dumps("X"), 6)

    def place(self, x, y, w=None, h=None, keep_ratio=True, is_text=False):
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
        self.key("Escape"); self.key("Escape")
        self.key("t")
        if not self.t.wait("document.activeElement && document.activeElement.isContentEditable", 6):
            raise RuntimeError("kotak teks tidak terbuka")
        self.key("a", ctrl=True)
        self.type(text)
        self.key("Escape")
        time.sleep(0.6)
        if font:
            self.button("t.startsWith('Toggle font selector')")
            box = self.t.wait("""(()=>{const i=[...document.querySelectorAll('input')].find(i=>i.getBoundingClientRect().x<420&&i.getBoundingClientRect().width>0&&/font|try|search/i.test((i.placeholder||'')+(i.getAttribute('aria-label')||'')));
                if(!i)return null;const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""", 6)
            self.click(box[0], box[1]); self.key("a", ctrl=True); self.type(font)
            time.sleep(1.5)
            self.button("t.split(String.fromCharCode(10))[0].trim()===%s||t.startsWith(%s+',')" % (json.dumps(font), json.dumps(font)), wait=10)
            time.sleep(1)
        if size:
            p = self.t.ev("""(()=>{const i=document.querySelector('input[aria-label="Font size"]')||[...document.querySelectorAll('input')].find(i=>{const r=i.getBoundingClientRect();return r.y<120&&r.width<80&&r.width>20});
                if(!i)return null;const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""")
            if p:
                self.click(p[0], p[1], 3); self.key("a", ctrl=True); self.type(str(size)); self.key("Enter"); time.sleep(0.8)
        if color:
            self.set_text_color(color)
        if bold:
            self.set_bold(True)
        if align:
            self.set_align(align)
        self.place(x, y, w, is_text=True)

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
        self.click(inp[0], inp[1], 3); self.key("a", ctrl=True); self.type(hex_color.lstrip("#")); self.key("Enter")
        time.sleep(0.8)
        self.key("Escape")

    def set_title(self, title):
        p = self.t.ev("""(()=>{const i=document.querySelector('input[aria-label="Design title"]');if(!i)return null;
            const r=i.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()""")
        if p:
            self.click(p[0], p[1]); self.key("a", ctrl=True); self.type(title); self.key("Enter")


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
            ed.click(bx, by, 3); ed.key("a", ctrl=True); ed.type(str(v))
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
        time.sleep(3)
        shot = tab.screenshot(Path.home() / ".creative-mcp" / "canva_native_last.png")
        return {"ok": not errors, "design_url": tab.ev("location.href"), "added": done, "errors": errors, "screenshot": shot}
    finally:
        tab.ws.close()  # leave the editor tab open for the user
