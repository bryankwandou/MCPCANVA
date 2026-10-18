"""Convert an HTML design into a canva_native spec: every text node becomes a native Canva text box and every
<img> a native Canva image, at the position/font/size/colour the browser actually rendered. Whatever is left
(shapes, gradients, SVG decoration) is rendered once, without the text and images, as the background image.

Markup hints (optional):
  data-canva="raster"  keep this element (and its text) inside the background image, e.g. a rotated code window
  data-canva="skip"    leave this element out entirely
Units: the page is laid out at the design size in CSS px (e.g. 3000x1000).
"""
from __future__ import annotations

import base64
import json
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

from .canva_browser import _chrome

PORT = 9333
# Canva's font size field is in pt: 1 CSS px = 0.75 pt (measured: Alfa Slab One 300px in HTML = 225 in Canva)
PX_TO_CANVA = 0.75
CANVA_LINE = 1.4  # Canva's default line spacing

_COLLECT = r"""(async()=>{await document.fonts.ready;
const root=document.querySelector('[data-canva-root]')||document.body, R=root.getBoundingClientRect();
const skip=e=>e.closest('[data-canva="raster"],[data-canva="skip"]');
const rgb2hex=c=>{const m=c.match(/[\d.]+/g);return '#'+m.slice(0,3).map(v=>(+v).toString(16).padStart(2,'0')).join('').toUpperCase()};
const out=[];
for(const img of root.querySelectorAll('img')){ if(skip(img))continue; const r=img.getBoundingClientRect();
  out.push({type:'image',src:img.getAttribute('src'),x:r.x-R.x,y:r.y-R.y,w:r.width,h:r.height});}
const tw=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let n;
while(n=tw.nextNode()){ const t=n.textContent.replace(/\s+/g,' ').trim(); if(!t)continue; const el=n.parentElement;
  if(skip(el))continue; const cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none')continue;
  const raw=n.textContent, a=raw.search(/\S/), b=raw.length-raw.split('').reverse().join('').search(/\S/);
  const rg=document.createRange(); rg.setStart(n,a); rg.setEnd(n,b); const rects=[...rg.getClientRects()].filter(r=>r.width>1);
  if(!rects.length)continue;
  const x0=Math.min(...rects.map(r=>r.x)),x1=Math.max(...rects.map(r=>r.right)),y0=Math.min(...rects.map(r=>r.y)),y1=Math.max(...rects.map(r=>r.bottom));
  out.push({type:'text',text:t,font:cs.fontFamily.split(',')[0].replace(/["']/g,'').trim(),px:parseFloat(cs.fontSize),
    weight:+cs.fontWeight,italic:cs.fontStyle==='italic',color:rgb2hex(cs.color),x:x0-R.x,y:y0-R.y,w:x1-x0,h:y1-y0,lines:rects.length});}
return {w:R.width,h:R.height,items:out};})()"""

# background pass: text invisible, images hidden, text effects off, raster islands kept as they are
_BG_CSS = """*:not([data-canva="raster"]):not([data-canva="raster"] *){color:transparent!important;text-shadow:none!important;
-webkit-text-stroke:0!important;caret-color:transparent!important}
img:not([data-canva="raster"] img){visibility:hidden!important}[data-canva="skip"]{visibility:hidden!important}"""


class _Headless:
    def __init__(self, w: int, h: int):
        import websocket
        self.tmp = tempfile.mkdtemp(prefix="html2canva-")
        self.p = subprocess.Popen([_chrome(), "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={self.tmp}",
                                   "--hide-scrollbars", f"--window-size={w},{h}", "about:blank"],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(40):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json", timeout=2))
                page = next(t for t in tabs if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError("headless Chrome tidak jalan")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], suppress_origin=True, timeout=120)
        self.n = 0
        self.send("Emulation.setDeviceMetricsOverride", {"width": w, "height": h, "deviceScaleFactor": 1, "mobile": False})

    def send(self, m, p=None):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": m, "params": p or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.n:
                if "error" in r:
                    raise RuntimeError(r["error"])
                return r.get("result", {})

    def ev(self, js):
        return self.send("Runtime.evaluate", {"expression": js, "returnByValue": True, "awaitPromise": True})["result"].get("value")

    def close(self):
        try:
            self.ws.close()
        finally:
            self.p.kill()
            shutil.rmtree(self.tmp, ignore_errors=True)


def convert(html_path: str, out_dir: str | None = None, width: int = 3000, height: int = 1000,
            bg_scale: int = 2, title: str | None = None) -> dict:
    """Render html_path and return a canva_native spec (also written to <out_dir>/<name>.canva.json)."""
    html = Path(html_path).resolve()
    out = Path(out_dir).resolve() if out_dir else html.parent / (html.stem + "-canva")
    out.mkdir(parents=True, exist_ok=True)
    hb = _Headless(width, height)
    try:
        hb.send("Page.enable")
        hb.send("Page.navigate", {"url": html.as_uri()})
        time.sleep(2)
        hb.ev("new Promise(r=>document.readyState==='complete'?r():addEventListener('load',r))")
        data = hb.ev(_COLLECT)
        # background without text/images, at bg_scale for print sharpness
        hb.ev("(()=>{const s=document.createElement('style');s.textContent=%s;document.head.appendChild(s)})()" % json.dumps(_BG_CSS))
        time.sleep(0.5)
        hb.send("Emulation.setDeviceMetricsOverride", {"width": width, "height": height, "deviceScaleFactor": bg_scale, "mobile": False})
        time.sleep(1)
        png = hb.send("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": width, "height": height, "scale": 1}})
        bg = out / (html.stem + "-latar.png")
        bg.write_bytes(base64.b64decode(png["data"]))
    finally:
        hb.close()

    elements = [{"type": "image", "path": str(bg), "x": 0, "y": 0, "w": width}]
    for it in data["items"]:
        if it["type"] == "image":
            src = (html.parent / it["src"]).resolve()
            elements.append({"type": "image", "path": str(src), "x": round(it["x"]), "y": round(it["y"]), "w": round(it["w"])})
    for it in data["items"]:
        if it["type"] != "text":
            continue
        size = round(it["px"] * PX_TO_CANVA, 1)
        box_h = it["px"] * CANVA_LINE * it["lines"]
        elements.append({"type": "text", "text": it["text"], "font": it["font"], "size": size, "color": it["color"],
                         "bold": it["weight"] >= 700 and it["font"] not in ("Alfa Slab One", "Archivo Black", "Anton"),
                         "x": round(it["x"]), "y": round(it["y"] + it["h"] / 2 - box_h / 2 + it["px"] * 0.12),
                         "w": round(it["w"] * 1.12 + 24)})  # slack so Canva's metrics never wrap; text is left-aligned
    spec = {"title": title or html.stem, "width": width, "height": height, "source_html": str(html), "elements": elements}
    (out / (html.stem + ".canva.json")).write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    return spec
