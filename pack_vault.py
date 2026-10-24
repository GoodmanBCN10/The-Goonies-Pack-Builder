import base64
import json
import marshal
import mimetypes
import os
import zlib
from pathlib import Path
from typing import Dict, Tuple

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
CATALOG_PATH = BASE_DIR / "catalog.json"
BUILDER_PATH = BASE_DIR / "builder.py"
APP_PATH = BASE_DIR / "app.py"
OUT_VAULT_PY = BASE_DIR / "_vault.py"

MIME_MAP = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".svg": "image/svg+xml",
    ".json": "application/json; charset=utf-8",
}


def build_vault() -> None:
    raw_key = AESGCM.generate_key(bit_length=256)
    mask = os.urandom(32)
    masked_key = bytes(a ^ b for a, b in zip(raw_key, mask))
    aes = AESGCM(raw_key)

    def seal_bytes(plain: bytes) -> str:
        compressed = zlib.compress(plain, level=9)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, compressed, b"GPB-VAULT-V1")
        return base64.b85encode(nonce + ct).decode("ascii")

    # 1. Cifrar catalog.json (minificado)
    cat_obj = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    cat_bytes = json.dumps(cat_obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sealed_catalog = seal_bytes(cat_bytes)

    # 2. Cifrar todos los archivos de static/
    sealed_assets: Dict[str, Tuple[str, str]] = {}
    for p in sorted(STATIC_DIR.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(STATIC_DIR).as_posix()
        mime = MIME_MAP.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        sealed_assets[rel] = (mime, seal_bytes(p.read_bytes()))

    # 3. Compilar y cifrar con AES-256-GCM el código de builder.py y app.py para ejecución en RAM
    builder_code = compile(BUILDER_PATH.read_text(encoding="utf-8"), "<gpb_builder>", "exec", optimize=2)
    sealed_builder = seal_bytes(marshal.dumps(builder_code))

    app_code = compile(APP_PATH.read_text(encoding="utf-8"), "<gpb_app>", "exec", optimize=2)
    sealed_app = seal_bytes(marshal.dumps(app_code))

    code = f'''# Auto-generated encrypted memory vault for The Goonies Pack Builder
import base64
import json
import marshal
import os
import sys
import types
import zlib
from typing import Any, Dict, Optional, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_M = {list(mask)!r}
_K = {list(masked_key)!r}
_C = {sealed_catalog!r}
_A: Dict[str, Tuple[str, str]] = {sealed_assets!r}
_B_MOD = {sealed_builder!r}
_APP_MOD = {sealed_app!r}


def _get_aes() -> AESGCM:
    k = bytes(a ^ b for a, b in zip(_K, _M))
    return AESGCM(k)


def _unseal(blob_b85: str) -> bytes:
    raw = base64.b85decode(blob_b85.encode("ascii"))
    nonce, ct = raw[:12], raw[12:]
    compressed = _get_aes().decrypt(nonce, ct, b"GPB-VAULT-V1")
    return zlib.decompress(compressed)


def get_catalog_dict() -> Dict[str, Any]:
    return json.loads(_unseal(_C).decode("utf-8"))


def get_static_asset(rel_path: str) -> Optional[Tuple[bytes, str]]:
    clean = rel_path.lstrip("/").replace("\\\\", "/")
    if not clean:
        clean = "index.html"
    entry = _A.get(clean)
    if not entry:
        return None
    mime, b85 = entry
    return _unseal(b85), mime


def seal_cache_data(data: Any) -> bytes:
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    comp = zlib.compress(raw, level=6)
    nonce = os.urandom(12)
    return nonce + _get_aes().encrypt(nonce, comp, b"GPB-CACHE-V1")


def unseal_cache_data(blob: bytes) -> Any:
    nonce, ct = blob[:12], blob[12:]
    comp = _get_aes().decrypt(nonce, ct, b"GPB-CACHE-V1")
    return json.loads(zlib.decompress(comp).decode("utf-8"))


def boot_app() -> None:
    # Desencriptar y cargar 'builder' directamente en memoria RAM sin ningún .pyc en disco
    b_mod = types.ModuleType("builder")
    b_mod.__file__ = "<hermetic_builder>"
    sys.modules["builder"] = b_mod
    b_code = marshal.loads(_unseal(_B_MOD))
    exec(b_code, b_mod.__dict__)

    # Desencriptar y cargar 'app' directamente en memoria RAM
    a_mod = types.ModuleType("app_runtime")
    a_mod.__file__ = "<hermetic_app>"
    sys.modules["app_runtime"] = a_mod
    a_code = marshal.loads(_unseal(_APP_MOD))
    exec(a_code, a_mod.__dict__)
    a_mod.main()
'''
    OUT_VAULT_PY.write_text(code, encoding="utf-8")
    print(f"Vault hermético generado en {OUT_VAULT_PY.name} (recursos + builder.py + app.py cifrados con AES-256-GCM).")


if __name__ == "__main__":
    build_vault()
