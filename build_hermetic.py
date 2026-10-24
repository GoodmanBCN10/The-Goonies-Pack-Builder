import glob
import subprocess
import sys
from pathlib import Path

from pack_vault import build_vault

BASE_DIR = Path(__file__).resolve().parent


def run_step(cmd: list, desc: str) -> None:
    print(f"\n[HERMETIC BUILD] {desc}...")
    subprocess.run(cmd, cwd=str(BASE_DIR), check=True)


def main() -> None:
    # 1. Generar _vault.py cifrado con AES-256-GCM (contiene catalog.json, static/*, builder.py y app.py)
    build_vault()

    entry_boot_py = BASE_DIR / "_entry_boot.py"
    entry_boot_py.write_text(
        """# Stub de arranque hermético (todas las librerías quedan enlazadas; la lógica real vive en _vault.pyd)
import argparse
import base64
import concurrent.futures
import ctypes
import fnmatch
import http.cookies
import http.server
import json
import marshal
import os
import pathlib
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import types
import urllib.parse
import webbrowser
import zipfile
import zlib
import requests
import webview
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import _vault

if __name__ == "__main__":
    _vault.boot_app()
""",
        encoding="utf-8",
    )

    try:
        # 2. Compilar _vault.py a binario C nativo (.pyd) con Nuitka si aún no existe o si se actualizó
        for old_pyd in glob.glob(str(BASE_DIR / "_vault*.pyd")):
            try:
                Path(old_pyd).unlink()
            except Exception:
                pass

        run_step(
            [
                sys.executable,
                "-m",
                "nuitka",
                "--module",
                "--assume-yes-for-downloads",
                "--remove-output",
                "_vault.py",
            ],
            "Compilando bóveda AES-256 (_vault.py) a código máquina C nativo (.pyd)",
        )

        # Eliminar _vault.py en texto plano para que solo quede el binario C compilado (_vault.*.pyd)
        vault_py = BASE_DIR / "_vault.py"
        if vault_py.exists():
            vault_py.unlink()

        pyd_files = glob.glob(str(BASE_DIR / "_vault*.pyd"))
        if not pyd_files:
            raise RuntimeError("No se encontró el binario compilado _vault*.pyd")

        # 3. Empaquetar con PyInstaller SIN incluir catalog.json, SIN static/, SIN builder.py y SIN app.py
        pyi_cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",
            "--icon",
            "static/logo.ico",
            "--version-file",
            "version_info.txt",
            "--name",
            "TheGooniesPackBuilder",
            "_entry_boot.py",
        ]
        run_step(pyi_cmd, "Empaquetando dist\\TheGooniesPackBuilder.exe hermético")

    finally:
        for f in (BASE_DIR / "_vault.py", entry_boot_py, BASE_DIR / "_vault.pyi"):
            if f.exists():
                try:
                    f.unlink()
                except Exception:
                    pass
        for pyd in glob.glob(str(BASE_DIR / "_vault*.pyd")):
            try:
                Path(pyd).unlink()
            except Exception:
                pass

    print("\n==============================================================")
    print("  COMPILACIÓN HERMÉTICA COMPLETADA CON ÉXITO")
    print("  Ejecutable blindado en: dist\\TheGooniesPackBuilder.exe")
    print("==============================================================")


if __name__ == "__main__":
    main()
