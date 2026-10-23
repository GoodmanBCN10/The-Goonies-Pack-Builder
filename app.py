import argparse
import json
import os
import socket
import subprocess
import sys
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from builder import BASE_DIR, BUNDLE_DIR, CACHE_DIR, PackBuilderEngine, eject_sd_drive, list_sd_drives

STATIC_DIR = BUNDLE_DIR / "static" if (BUNDLE_DIR / "static").exists() else BASE_DIR / "static"
engine = PackBuilderEngine()


class CreatorRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format, *args):
        pass

    def _send_json(self, data: dict, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
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

        if path == "/api/state":
            qs = parse_qs(parsed.query)
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

        if path == "/" or path == "":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

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


def find_free_port(preferred: int = 8765) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", preferred)) != 0:
            return preferred
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

    port = args.port or find_free_port(8765)
    server = start_server(port)
    engine.start_background_github_sync()
    url = f"http://127.0.0.1:{port}"

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
