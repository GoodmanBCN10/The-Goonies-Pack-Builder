import argparse
import json
import os
import secrets
import socket
import subprocess
import sys
import threading
import webbrowser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from builder import BASE_DIR, BUNDLE_DIR, CACHE_DIR, PackBuilderEngine, eject_sd_drive, list_sd_drives

STATIC_DIR = BUNDLE_DIR / "static" if (BUNDLE_DIR / "static").exists() else BASE_DIR / "static"
SESSION_TOKEN = secrets.token_urlsafe(32)
engine = PackBuilderEngine()


class CreatorRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _is_authorized(self, parsed_qs: dict) -> bool:
        if parsed_qs.get("__t", [""])[0] == SESSION_TOKEN:
            return True
        cookie_hdr = self.headers.get("Cookie", "")
        if cookie_hdr:
            c = SimpleCookie()
            try:
                c.load(cookie_hdr)
                if "__gpb_sid" in c and c["__gpb_sid"].value == SESSION_TOKEN:
                    return True
            except Exception:
                pass
        return False

    def _send_json(self, data: dict, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _send_bytes(self, raw: bytes, content_type: str, set_session_cookie: bool = False) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        if set_session_cookie:
            self.send_header("Set-Cookie", f"__gpb_sid={SESSION_TOKEN}; Path=/; HttpOnly; SameSite=Strict")
        self.end_headers()
        self.wfile.write(raw)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if not self._is_authorized(qs):
            self.send_response(403)
            self.end_headers()
            return

        set_cookie = qs.get("__t", [""])[0] == SESSION_TOKEN

        if path == "/api/state":
            fw = qs.get("fw", [""])[0]
            base_tag = qs.get("base", [""])[0]
            resolved = engine.resolve_for_firmware(fw, base_tag)
            cache_files = list(CACHE_DIR.glob("*")) if CACHE_DIR.exists() else []
            cache_size = sum(f.stat().st_size for f in cache_files if f.is_file())
            resolved["cache_size_mb"] = round(cache_size / (1024 * 1024), 1)
            resolved["cache_count"] = len(cache_files)
            resolved["gh_sync"] = engine.gh_sync_state
            return self._send_json(resolved)

        if path == "/api/drives":
            return self._send_json({"drives": list_sd_drives()})

        if path == "/api/build/status":
            return self._send_json(engine.status)

        rel_asset = "index.html" if path in ("/", "") else path.lstrip("/")
        try:
            import _vault

            asset_res = _vault.get_static_asset(rel_asset)
            if asset_res:
                raw_bytes, mime = asset_res
                return self._send_bytes(raw_bytes, mime, set_session_cookie=set_cookie)
        except Exception:
            pass

        disk_file = (STATIC_DIR / rel_asset).resolve()
        if disk_file.is_file() and str(disk_file).startswith(str(STATIC_DIR.resolve())):
            ext = disk_file.suffix.lower()
            mime_map = {
                ".html": "text/html; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".png": "image/png",
                ".ico": "image/x-icon",
            }
            return self._send_bytes(
                disk_file.read_bytes(),
                mime_map.get(ext, "application/octet-stream"),
                set_session_cookie=set_cookie,
            )

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if not self._is_authorized(qs):
            self.send_response(403)
            self.end_headers()
            return

        try:
            body = self._read_json_body()
        except Exception as e:
            return self._send_json({"error": f"JSON inválido: {e}"}, status=400)

        if path == "/api/sync":
            try:
                res = engine.sync_with_github()
                return self._send_json({"ok": True, **res})
            except Exception as e:
                return self._send_json({"ok": False, "error": str(e)}, status=500)

        if path == "/api/build":
            try:
                engine.build_pack_async(body)
                return self._send_json({"ok": True})
            except Exception as e:
                return self._send_json({"ok": False, "error": str(e)}, status=400)

        if path == "/api/open-drive":
            drive = body.get("drive", "")
            if drive and Path(drive).exists():
                subprocess.Popen(["explorer", os.path.normpath(drive)])
                return self._send_json({"ok": True})
            return self._send_json({"ok": False, "error": "Unidad no encontrada"}, status=404)

        if path == "/api/eject-drive":
            drive = body.get("drive", "")
            ok, msg = eject_sd_drive(drive)
            return self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)

        if path == "/api/clear-cache":
            try:
                if CACHE_DIR.exists():
                    for f in CACHE_DIR.iterdir():
                        if f.is_file():
                            f.unlink()
                return self._send_json({"ok": True})
            except Exception as e:
                return self._send_json({"ok": False, "error": str(e)}, status=500)

        return self._send_json({"error": "Ruta no encontrada"}, status=404)


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_server(port: int) -> HTTPServer:
    server = HTTPServer(("127.0.0.1", port), CreatorRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main():
    parser = argparse.ArgumentParser(description="The Goonies Pack Builder")
    parser.add_argument("--headless", action="store_true", help="Ejecutar solo servidor web local sin ventana nativa")
    parser.add_argument("--port", type=int, default=0, help="Puerto HTTP local")
    args = parser.parse_args()

    port = args.port or find_free_port()
    server = start_server(port)
    engine.start_background_github_sync()
    url = f"http://127.0.0.1:{port}/?__t={SESSION_TOKEN}"

    if args.headless:
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            server.shutdown()
        return

    try:
        import webview

        window = webview.create_window(
            title="Goonies Pack Builder",
            url=url,
            width=1280,
            height=860,
            min_size=(1024, 700),
            background_color="#0b0f19",
        )
        webview.start(debug=False)
        server.shutdown()
    except Exception:
        webbrowser.open(url)
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            server.shutdown()


if __name__ == "__main__":
    main()
