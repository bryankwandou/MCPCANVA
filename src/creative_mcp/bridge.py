"""Local bridge between the web editor (Vercel or local) and CapCut drafts on this PC.

Runs on 127.0.0.1 only and every API call needs the random token printed in the
editor link, so other websites cannot read or change your projects.

Edits are kept as a *pending scene* (~/.creative-mcp/scenes/<draft>.json) while
you preview; nothing touches the CapCut draft until /api/deploy is called.
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
import secrets
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import cache, capcut, scene

HOME = cache.HOME
SCENES = HOME / "scenes"
DESIGNS = HOME / "designs"
EDITOR_DIR = Path(__file__).resolve().parent / "editor"
MEDIA_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".jpg", ".jpeg", ".png", ".gif", ".webp",
             ".mp3", ".wav", ".m4a", ".aac", ".ogg"}

_server: ThreadingHTTPServer | None = None
_lock = threading.Lock()


def token() -> str:
    f = HOME / "bridge.json"
    try:
        return json.loads(f.read_text())["token"]
    except (OSError, ValueError, KeyError):
        HOME.mkdir(parents=True, exist_ok=True)
        t = secrets.token_urlsafe(24)
        f.write_text(json.dumps({"token": t}))
        return t


def port() -> int:
    return int(os.getenv("CREATIVE_BRIDGE_PORT", "8765"))


def _safe(name: str) -> str:
    return re.sub(r"[^\w\- .]", "_", name)


def _scene_file(draft: str) -> Path:
    return SCENES / f"{_safe(draft)}.json"


def get_scene(draft: str) -> dict:
    f = _scene_file(draft)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    s = scene.from_draft(draft)
    s["version"] = 0
    return s


def put_scene(s: dict) -> dict:
    with _lock:
        SCENES.mkdir(parents=True, exist_ok=True)
        cur = _scene_file(s["draft"])
        old_v = json.loads(cur.read_text(encoding="utf-8")).get("version", 0) if cur.exists() else 0
        s["version"] = old_v + 1
        cur.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    return {"version": s["version"]}


def deploy(draft: str) -> dict:
    res = scene.apply_to_draft(get_scene(draft))
    _scene_file(draft).unlink(missing_ok=True)
    cache.clear("capcut:")
    return res


def discard(draft: str) -> dict:
    _scene_file(draft).unlink(missing_ok=True)
    return {"ok": True}


def media_dirs() -> list[Path]:
    env = os.getenv("CREATIVE_MEDIA_DIRS")
    if env:
        return [Path(p).expanduser() for p in env.split(os.pathsep) if p]
    h = Path.home()
    return [h / d for d in ("Videos", "Movies", "Pictures", "Music", "Downloads", "Desktop")]


def library(refresh: bool = False) -> list[dict]:
    if not refresh:
        hit = cache.get("library", 600)
        if hit is not None:
            return hit
    items = []
    for root in media_dirs():
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if len(items) >= 2000:
                break
            if p.suffix.lower() in MEDIA_EXT and len(p.relative_to(root).parts) <= 3:
                kind = mimetypes.guess_type(p.name)[0] or ""
                items.append({"path": str(p), "name": p.name,
                              "type": "video" if kind.startswith("video") else
                              "audio" if kind.startswith("audio") else "photo"})
    return cache.put("library", items)


def _allowed_media(path: str) -> bool:
    p = Path(path).resolve()
    if p.suffix.lower() not in MEDIA_EXT:
        return False
    roots = [d.resolve() for d in media_dirs()] + [capcut.drafts_dir().resolve()]
    if any(p.is_relative_to(r) for r in roots):
        return True
    for f in SCENES.glob("*.json"):  # files already used in a project
        if path in f.read_text(encoding="utf-8"):
            return True
    try:
        return any(path in json.dumps(capcut.load(d["name"])) for d in capcut.list_drafts())
    except Exception:
        return False


def _design_file(design_id: str) -> Path:
    return DESIGNS / f"{_safe(design_id)}.json"


def list_designs() -> list[dict]:
    DESIGNS.mkdir(parents=True, exist_ok=True)
    f_seed = _design_file("artisan-coffee-masterpiece")
    if not f_seed.exists():
        seed_data = {
            "id": "artisan-coffee-masterpiece",
            "title": "Artisan Coffee Masterpiece",
            "width": 1080,
            "height": 1350,
            "updated": int(time.time() * 1000),
            "thumb": "assets/artisan_coffee.jpg",
            "pptx": "assets/artisan-coffee-canva-template.pptx",
            "pages": [{
                "id": "page-1",
                "bg": "#120D0A",
                "title": "Masterpiece Showcase",
                "elements": [
                    {"id": "el-1", "type": "rect", "x": 70, "y": 50, "w": 330, "h": 42, "fill": "#D4A373", "radius": 999},
                    {"id": "el-2", "type": "text", "x": 70, "y": 58, "w": 330, "h": 26, "text": "SPECIALTY ROASTERY & CAFE", "fontSize": 13, "color": "#120D0A", "bold": True, "align": "center"},
                    {"id": "el-3", "type": "text", "x": 70, "y": 105, "w": 940, "h": 85, "text": "ARTISAN COFFEE MASTERPIECE", "fontSize": 40, "color": "#FDFBF7", "bold": True},
                    {"id": "el-4", "type": "text", "x": 70, "y": 195, "w": 940, "h": 45, "text": "Racikan Biji Kopi Arabica Pilihan dengan Aroma Autentik & Tekstur Lembut", "fontSize": 17, "color": "#C8BDB0"},
                    {"id": "el-5", "type": "rect", "x": 64, "y": 244, "w": 952, "h": 442, "fill": "#D4A373", "radius": 24},
                    {"id": "el-6", "type": "image", "x": 70, "y": 250, "w": 940, "h": 430, "src": "assets/artisan_coffee.jpg", "radius": 20},
                    {"id": "el-7", "type": "star", "x": 860, "y": 225, "w": 140, "h": 140, "fill": "#E76F51"},
                    {"id": "el-8", "type": "text", "x": 860, "y": 260, "w": 140, "h": 60, "text": "DISKON\n25%", "fontSize": 18, "color": "#FFFFFF", "bold": True, "align": "center"},
                    {"id": "el-9", "type": "rect", "x": 70, "y": 998, "w": 940, "h": 70, "fill": "#D4A373", "radius": 20},
                    {"id": "el-10", "type": "text", "x": 70, "y": 1020, "w": 940, "h": 36, "text": "KUNJUNGI KEDAI ATAU PESAN ONLINE SEKARANG", "fontSize": 19, "color": "#120D0A", "bold": True, "align": "center"}
                ]
            }]
        }
        f_seed.write_text(json.dumps(seed_data, indent=2), encoding="utf-8")
    out = []
    for f in DESIGNS.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        out.append({k: d.get(k) for k in ("id", "title", "width", "height", "updated", "thumb", "pptx")})
    return out


def catalog() -> dict:
    """Cheap synchronous catalog for the dashboard (Canva part comes from the MCP cache)."""
    me = cache.get("canva:me", 86400 * 7) or {}
    designs = cache.get("canva:designs", 86400) or {}
    canva = {"user": me.get("profile", {}).get("profile", {}).get("display_name"),
             "capabilities": me.get("capabilities", {}).get("capabilities", []),
             "recent_designs": [{"id": d["id"], "title": d.get("title"),
                                 "edit_url": d.get("urls", {}).get("edit_url")}
                                for d in designs.get("items", [])[:20]]}
    if not me:
        canva["error"] = "Belum ada data Canva di cache. Jalankan tool `catalog` dari AI setelah login."
    try:
        drafts = capcut.list_drafts()
    except Exception:
        drafts = []
    return {"canva": canva, "capcut_projects": drafts}


def design_to_canva(design: dict) -> dict:
    import asyncio

    from .canva import CanvaClient
    from .templates import design_to_pptx

    path = design_to_pptx(design, HOME / "exports")
    try:
        res = asyncio.run(CanvaClient().import_file(path, design.get("title")))
    except Exception as e:
        return {"pptx": path, "error": str(e)}
    return {"pptx": path, "canva": res}


def canva_desktop_path() -> Path | None:
    candidates = [
        Path.home() / "AppData/Local/Programs/Canva/Canva.exe",
        Path("C:/Program Files/Canva/Canva.exe"),
        Path("C:/Program Files (x86)/Canva/Canva.exe"),
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def launch_canva(data: dict | None = None) -> dict:
    import subprocess
    import sys

    data = data or {}
    url = data.get("url") or "canva://"
    try:
        if sys.platform == "win32":
            p = canva_desktop_path()
            if p and not data.get("url"):
                subprocess.Popen([str(p)])
                return {"ok": True, "message": "Canva Desktop dibuka melalui Canva.exe", "path": str(p)}
            os.startfile(url)
            return {"ok": True, "message": "Canva Desktop dibuka melalui protokol", "target": url}
        return {"error": "Hanya didukung di Windows"}
    except Exception as e:
        return {"error": str(e)}


def mcp_status() -> dict:
    c_path = canva_desktop_path()
    cat = catalog()
    return {
        "status": "connected",
        "canva_desktop_installed": c_path is not None,
        "canva_desktop_path": str(c_path) if c_path else None,
        "tools": [
            "canva_list_designs",
            "canva_create_design",
            "canva_get_design",
            "canva_get_pages",
            "canva_upload_asset",
            "canva_export",
            "canva_import_file",
            "canva_import_url",
            "canva_open_editor",
            "canva_open_desktop",
            "canva_create_showcase_template",
            "canva_autofill",
            "canva_resize",
            "catalog",
            "desktop_screenshot",
            "desktop_click",
            "desktop_type",
        ],
        "canva_account": cat.get("canva", {}),
    }



class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Bridge-Token, Range")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):  # noqa: N802
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _q(self):
        u = urllib.parse.urlparse(self.path)
        return u.path, dict(urllib.parse.parse_qsl(u.query))

    def _authed(self, q) -> bool:
        t = self.headers.get("X-Bridge-Token") or q.get("token", "")
        return secrets.compare_digest(t, token())

    def do_GET(self):  # noqa: N802
        path, q = self._q()
        if not path.startswith(("/api/", "/media")):  # static Studio pages
            f = (EDITOR_DIR / (path.lstrip("/") or "index.html")).resolve()
            if f.is_relative_to(EDITOR_DIR) and f.is_file():
                return self._file(f)
            return self._json({"error": "not found"}, 404)
        if not self._authed(q):
            return self._json({"error": "bad token"}, 401)
        try:
            if path == "/api/drafts":
                return self._json(capcut.list_drafts())
            if path == "/api/scene":
                return self._json(get_scene(q["draft"]))
            if path == "/api/version":
                f = _scene_file(q["draft"])
                v = json.loads(f.read_text(encoding="utf-8")).get("version", 0) if f.exists() else 0
                return self._json({"version": v})
            if path == "/api/library":
                return self._json(library(q.get("refresh") == "1"))
            if path == "/api/designs":
                return self._json(list_designs())
            if path == "/api/design":
                return self._json(json.loads(_design_file(q["id"]).read_text(encoding="utf-8")))
            if path == "/api/capcut-library":
                from . import capcut_library
                return self._json(capcut_library.list_items())
            if path == "/api/catalog":
                return self._json(catalog())
            if path == "/api/mcp/status":
                return self._json(mcp_status())
            if path == "/media":
                if not _allowed_media(q.get("path", "")):
                    return self._json({"error": "not allowed"}, 403)
                return self._file(Path(q["path"]))
            self._json({"error": "not found"}, 404)
        except Exception as e:  # report to the editor instead of crashing
            self._json({"error": str(e)}, 500)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(n) or b"{}")

    def do_PUT(self):  # noqa: N802
        path, q = self._q()
        if not self._authed(q):
            return self._json({"error": "bad token"}, 401)
        if path == "/api/scene":
            return self._json(put_scene(self._body()))
        if path == "/api/design":
            d = self._body()
            DESIGNS.mkdir(parents=True, exist_ok=True)
            _design_file(d["id"]).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            return self._json({"ok": True})
        self._json({"error": "not found"}, 404)

    def do_DELETE(self):  # noqa: N802
        path, q = self._q()
        if not self._authed(q):
            return self._json({"error": "bad token"}, 401)
        if path == "/api/design":
            _design_file(q["id"]).unlink(missing_ok=True)
            return self._json({"ok": True})
        self._json({"error": "not found"}, 404)

    def do_POST(self):  # noqa: N802
        path, q = self._q()
        if not self._authed(q):
            return self._json({"error": "bad token"}, 401)
        try:
            if path == "/api/deploy":
                return self._json(deploy(q["draft"]))
            if path == "/api/discard":
                return self._json(discard(q["draft"]))
            if path == "/api/capcut-library/scan":
                from . import capcut_library
                return self._json(capcut_library.scan())
            if path == "/api/capcut/template":
                from . import templates
                b = self._body()
                return self._json(templates.build_capcut(
                    b["template"], b["name"], b["media"], b.get("title", ""), b.get("captions"),
                    b.get("cta", ""), b.get("music"), b.get("palette", "bold")))
            if path == "/api/design/canva":
                return self._json(design_to_canva(self._body()))
            if path == "/api/canva/launch":
                return self._json(launch_canva(self._body()))
            self._json({"error": "not found"}, 404)
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def _file(self, p: Path):
        if not p.exists():
            return self._json({"error": "missing file"}, 404)
        size = p.stat().st_size
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        start, end = 0, size - 1
        rng = self.headers.get("Range")
        m = re.match(r"bytes=(\d*)-(\d*)", rng or "")
        if m and size:
            start = int(m.group(1) or 0)
            end = min(int(m.group(2)) if m.group(2) else size - 1, size - 1)
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        else:
            self.send_response(200)
        self._cors()
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1 if size else 0))
        self.end_headers()
        with p.open("rb") as f:
            f.seek(start)
            left = end - start + 1
            while left > 0:
                chunk = f.read(min(1 << 16, left))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                left -= len(chunk)


def start() -> str:
    """Start the bridge once (idempotent); returns its base URL."""
    global _server
    if _server is None:
        _server = ThreadingHTTPServer(("127.0.0.1", port()), Handler)
        threading.Thread(target=_server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{port()}"


def studio_url() -> dict:
    base = start()
    frag = urllib.parse.urlencode({"bridge": base, "token": token()})
    out = {"local": f"{base}/#{frag}"}
    hosted = os.getenv("CREATIVE_EDITOR_URL")
    if hosted:
        out["vercel"] = f"{hosted.rstrip('/')}/#{frag}"
    return out


def editor_url(draft: str) -> dict:
    base = start()
    frag = urllib.parse.urlencode({"bridge": base, "token": token(), "draft": draft})
    out = {"local": f"{base}/video.html#{frag}"}
    hosted = os.getenv("CREATIVE_EDITOR_URL")  # e.g. https://my-editor.vercel.app
    if hosted:
        out["vercel"] = f"{hosted.rstrip('/')}/video.html#{frag}"
    return out
