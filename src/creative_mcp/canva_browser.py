"""Upload files into the user's Canva account through a logged-in Chrome (DevTools Protocol, port 9222).

Works without Canva Connect API credentials. Chrome is started with a persistent profile that is already
signed in to canva.com; files are dropped onto Canva's "Upload" dialog with a synthetic drag-and-drop
(Canva does not use a plain <input type=file>, so DOM.setFileInputFiles does not work).
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

PORT = int(os.getenv("CANVA_CDP_PORT", "9222"))
PROFILE = Path(os.getenv("CANVA_CDP_PROFILE", Path.home() / ".gemini" / "antigravity-browser-profile"))
BASE = f"http://127.0.0.1:{PORT}"
_UPLOAD_BTN = r"/^(upload|unggah)\b/i"


def _chrome() -> str | None:
    for p in (Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
              Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
              Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe"):
        if p.is_file():
            return str(p)
    return None


def _alive() -> bool:
    try:
        urllib.request.urlopen(BASE + "/json/version", timeout=3)
        return True
    except OSError:
        return False


def ensure_chrome() -> dict:
    """Start Chrome with the Canva profile and debug port if it is not already running."""
    if _alive():
        return {"running": True, "started": False}
    exe = _chrome()
    if not exe:
        return {"running": False, "error": "Google Chrome tidak ditemukan"}
    subprocess.Popen([exe, f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}", "https://www.canva.com/"])
    for _ in range(20):
        time.sleep(1)
        if _alive():
            return {"running": True, "started": True}
    return {"running": False, "error": f"Chrome tidak membuka port {PORT}"}


class _Tab:
    """A fresh Canva tab (old tabs can stop answering Runtime.evaluate)."""

    def __init__(self, url: str = "https://www.canva.com/"):
        import websocket

        req = urllib.request.Request(f"{BASE}/json/new?{url}", method="PUT")
        self.info = json.load(urllib.request.urlopen(req, timeout=10))
        time.sleep(6)
        self.ws = websocket.create_connection(self.info["webSocketDebuggerUrl"], suppress_origin=True, timeout=30)
        self.n = 0
        self.send("Page.bringToFront")
        self.send("Emulation.setDeviceMetricsOverride", {"width": 1600, "height": 900, "deviceScaleFactor": 1, "mobile": False})

    def send(self, method: str, params: dict | None = None) -> dict:
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.n:
                return r

    def ev(self, js: str):
        return self.send("Runtime.evaluate", {"expression": js, "returnByValue": True})["result"]["result"].get("value")

    def screenshot(self, path: Path) -> str:
        path.write_bytes(base64.b64decode(self.send("Page.captureScreenshot", {"format": "png"})["result"]["data"]))
        return str(path)

    def close(self):
        try:
            self.ws.close()
            urllib.request.urlopen(f"{BASE}/json/close/{self.info['id']}", timeout=5)
        except Exception:
            pass

    def wait(self, js: str, seconds: float = 40):
        end = time.time() + seconds
        while time.time() < end:
            v = self.ev(js)
            if v:
                return v
            time.sleep(1.5)
        return None


def status() -> dict:
    """Is Chrome up and is the Canva session signed in?"""
    st = ensure_chrome()
    if not st.get("running"):
        return st
    tab = _Tab()
    try:
        ready = tab.wait(f"document.title && Array.from(document.querySelectorAll('button,[role=button]')).some(b => {_UPLOAD_BTN}.test((b.innerText||'').trim()))", 30)
        info = tab.ev("({url: location.href, title: document.title})")
        return {**st, **(info or {}), "logged_in": bool(ready) and "/login" not in (info or {}).get("url", "")}
    finally:
        tab.close()


def upload(files: list[str], wait_s: int = 60) -> dict:
    """Upload local files (PPTX, PDF, PNG, JPG, MP4...) to Canva Uploads. PPTX/PDF become editable designs."""
    paths = [str(Path(f).expanduser().resolve()) for f in files]
    missing = [p for p in paths if not Path(p).is_file()]
    if missing:
        return {"ok": False, "error": "file tidak ada", "missing": missing}
    st = ensure_chrome()
    if not st.get("running"):
        return {"ok": False, **st}
    tab = _Tab()
    try:
        if not tab.wait(f"document.title && Array.from(document.querySelectorAll('button,[role=button]')).some(b => {_UPLOAD_BTN}.test((b.innerText||'').trim()))", 40):
            return {"ok": False, "error": "Beranda Canva tidak siap / belum login", "url": tab.ev("location.href")}
        tab.ev(f"Array.from(document.querySelectorAll('button,[role=button]')).find(b => {_UPLOAD_BTN}.test((b.innerText||'').trim())).click()")
        pos = tab.wait("""(() => { const b = Array.from(document.querySelectorAll('button')).find(b => /^upload files$|^unggah file/i.test(b.innerText.trim()));
            if (!b) return null; const r = b.getBoundingClientRect(); return [r.x + r.width / 2, r.y - 120]; })()""", 30)
        if not pos:
            return {"ok": False, "error": "dialog Upload tidak muncul"}
        data = {"items": [], "files": paths, "dragOperationsMask": 1}
        for t in ("dragEnter", "dragOver", "drop"):
            tab.send("Input.dispatchDragEvent", {"type": t, "x": pos[0], "y": pos[1], "data": data})
            time.sleep(0.4)
        names = [Path(p).name for p in paths]
        js = "(() => { const t = document.body.innerText; return %s.filter(n => t.includes(n)); })()" % json.dumps(names)
        seen: list = []
        end = time.time() + wait_s
        while time.time() < end:
            seen = tab.ev(js) or []
            if len(seen) == len(names) and "uploaded" in (tab.ev("document.body.innerText") or "").lower():
                break
            time.sleep(2)
        shot = tab.screenshot(Path.home() / ".creative-mcp" / "canva_upload_last.png")
        return {"ok": len(seen) == len(names), "uploaded": seen, "files": names, "screenshot": shot,
                "where": "Canva > Projects > Uploads (juga di Recent designs)"}
    finally:
        tab.close()
