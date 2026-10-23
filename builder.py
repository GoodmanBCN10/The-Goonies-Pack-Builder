import concurrent.futures
import ctypes
import fnmatch
import json
import os
import re
import shutil
import sys
import tempfile
import threading
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", BASE_DIR))
else:
    BASE_DIR = Path(__file__).resolve().parent
    BUNDLE_DIR = BASE_DIR

INTERNAL_CATALOG_PATH = BUNDLE_DIR / "catalog.json"
USER_CATALOG_PATH = BASE_DIR / ".cache" / "catalog_user.json"
GH_HTTP_CACHE_PATH = BASE_DIR / ".cache" / "gh_http_cache.json"
CACHE_DIR = BASE_DIR / ".cache" / "downloads"

# Carpetas que NUNCA se deben borrar en la raíz de la microSD
PROTECTED_SD_ROOT_ITEMS = {"emummc", "nintendo", "system volume information"}

# Carpetas típicas que identifican una microSD de Nintendo Switch / Hekate
SWITCH_MARKER_DIRS = {"emummc", "nintendo", "bootloader", "atmosphere", "switch"}


def parse_version(v_str: str) -> Tuple[int, ...]:
    """Convierte una cadena de versión (ej. '23.0.1', 'V2.2.0', '912ru', '12/02/2025') en una tupla comparable."""
    if not v_str:
        return (0,)
    cleaned = v_str.strip().lstrip("vV")
    # Detectar formato fecha MM/DD/YYYY (usado por JKSV)
    date_match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", cleaned)
    if date_match:
        mm, dd, yyyy = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
        return (yyyy, mm, dd)
    # Ignorar sufijos pre-release (-beta1, -alpha, -test) para que 0.7.14 sea mayor que 0.7.14-beta1
    base_part = re.split(r"-(?:alpha|beta|test|rc)", cleaned, flags=re.I)[0]
    nums = re.findall(r"\d+", base_part)
    if not nums:
        return (0,)
    return tuple(int(n) for n in nums)


def version_in_range(target: str, min_v: str = "0.0.0", max_v: str = "999.0.0") -> bool:
    t = parse_version(target)
    low = parse_version(min_v) if min_v else (0,)
    high = parse_version(max_v) if max_v else (999, 999, 999)

    def pad(tup: Tuple[int, ...]) -> Tuple[int, ...]:
        return tup + (0,) * max(0, 4 - len(tup))

    return pad(low) <= pad(t) <= pad(high)


def list_sd_drives() -> List[Dict[str, Any]]:
    """
    Detecta unidades montadas en Windows (especialmente la Switch conectada por Hekate -> USB Tools -> SD Card)
    y excluye estrictamente el disco del sistema operativo (C:\\).
    """
    drives_info: List[Dict[str, Any]] = []
    if os.name != "nt":
        return drives_info

    sys_drive = os.environ.get("SystemDrive", "C:").upper().rstrip("\\/")
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()

    for i in range(26):
        if not (bitmask & (1 << i)):
            continue
        letter = f"{chr(65 + i)}:"
        if letter.upper() == sys_drive:
            continue

        root_path = f"{letter}\\"
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(ctypes.c_wchar_p(root_path))
        # 2 = DRIVE_REMOVABLE (USB/SD/Hekate UMS), 3 = DRIVE_FIXED (algunos lectores USB se reportan como tipo 3)
        if drive_type not in (2, 3):
            continue

        p_root = Path(root_path)
        try:
            if not p_root.exists():
                continue
            # Excluir cualquier partición de Windows / PC con carpetas de sistema críticas
            if (p_root / "Windows").exists() or (p_root / "Program Files").exists():
                continue

            vol_name_buf = ctypes.create_unicode_buffer(261)
            fs_name_buf = ctypes.create_unicode_buffer(261)
            ctypes.windll.kernel32.GetVolumeInformationW(
                ctypes.c_wchar_p(root_path),
                vol_name_buf,
                261,
                None,
                None,
                None,
                fs_name_buf,
                261,
            )
            label = vol_name_buf.value or "Sin etiqueta"
            fs_type = fs_name_buf.value or "FAT32/exFAT"

            usage = shutil.disk_usage(root_path)
            total_gb = round(usage.total / (1024 ** 3), 1)
            free_gb = round(usage.free / (1024 ** 3), 1)

            existing_Names = {child.name.lower() for child in p_root.iterdir()}
        except Exception:
            continue

        has_emummc = "emummc" in existing_Names
        has_nintendo = "nintendo" in existing_Names
        matched_markers = existing_Names.intersection(SWITCH_MARKER_DIRS)
        is_removable = drive_type == 2
        is_switch_sd = len(matched_markers) > 0

        # Si es un disco fijo (drive_type == 3) y NO tiene ni una sola carpeta de Switch, no lo mostramos por seguridad
        if not is_removable and not is_switch_sd:
            continue

        detected_badges = []
        if has_emummc:
            detected_badges.append("emuMMC")
        if has_nintendo:
            detected_badges.append("Nintendo")
        if "bootloader" in existing_Names:
            detected_badges.append("Hekate")
        if "atmosphere" in existing_Names:
            detected_badges.append("Atmosphere")

        drives_info.append({
            "drive": root_path,
            "letter": letter,
            "label": label,
            "fs_type": fs_type,
            "total_gb": total_gb,
            "free_gb": free_gb,
            "is_removable": is_removable,
            "is_switch_sd": is_switch_sd,
            "has_emummc": has_emummc,
            "has_nintendo": has_nintendo,
            "detected_badges": detected_badges,
        })

    # Ordenar poniendo primero las unidades que ya tienen marcadores de Switch o son extraíbles
    drives_info.sort(key=lambda d: (not d["is_switch_sd"], not d["is_removable"], d["letter"]))
    return drives_info


def eject_sd_drive(drive_str: str) -> Tuple[bool, str]:
    """
    Expulsa de forma segura la unidad USB Mass Storage (UMS) en Windows (vaciando buffers y enviando
    IOCTL_STORAGE_EJECT_MEDIA), lo que hace que Hekate cierre automáticamente la sesión USB en la Switch.
    """
    if not drive_str:
        return False, "No hay ninguna unidad seleccionada."

    letter = Path(drive_str).drive.upper().rstrip("\\/")
    if not letter:
        return False, "Letra de unidad no válida."

    sys_drive = os.environ.get("SystemDrive", "C:").upper().rstrip("\\/")
    if letter == sys_drive:
        return False, "No se puede expulsar la unidad del sistema."

    # 1. Intentar expulsión directa por Win32 DeviceIoControl (envía comando SCSI Eject a Hekate UMS)
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    FILE_SHARE_READ = 0x00000001
    FILE_SHARE_WRITE = 0x00000002
    OPEN_EXISTING = 3

    FSCTL_LOCK_VOLUME = 0x00090018
    FSCTL_DISMOUNT_VOLUME = 0x00090020
    IOCTL_STORAGE_MEDIA_REMOVAL = 0x002D4804
    IOCTL_STORAGE_EJECT_MEDIA = 0x002D4808

    device_path = f"\\\\.\\{letter}"
    k32 = ctypes.windll.kernel32
    handle = k32.CreateFileW(
        ctypes.c_wchar_p(device_path),
        GENERIC_READ | GENERIC_WRITE,
        FILE_SHARE_READ | FILE_SHARE_WRITE,
        None,
        OPEN_EXISTING,
        0,
        None,
    )

    if handle != -1 and handle != 0xFFFFFFFFFFFFFFFF:
        try:
            bytes_returned = ctypes.c_ulong(0)
            k32.FlushFileBuffers(handle)

            # Intentar bloquear volumen (varios reintentos breves por si el antivirus está cerrando handles)
            locked = False
            for _ in range(5):
                if k32.DeviceIoControl(handle, FSCTL_LOCK_VOLUME, None, 0, None, 0, ctypes.byref(bytes_returned), None):
                    locked = True
                    break
                time.sleep(0.2)

            if locked:
                k32.DeviceIoControl(handle, FSCTL_DISMOUNT_VOLUME, None, 0, None, 0, ctypes.byref(bytes_returned), None)

            # Permitir extracción del medio (PREVENT_MEDIA_REMOVAL = False)
            pmr = ctypes.c_byte(0)
            k32.DeviceIoControl(
                handle,
                IOCTL_STORAGE_MEDIA_REMOVAL,
                ctypes.byref(pmr),
                ctypes.sizeof(pmr),
                None,
                0,
                ctypes.byref(bytes_returned),
                None,
            )

            ejected = k32.DeviceIoControl(
                handle, IOCTL_STORAGE_EJECT_MEDIA, None, 0, None, 0, ctypes.byref(bytes_returned), None
            )
            if ejected:
                return True, f"Consola ({letter}) desconectada de forma segura. Hekate cerrará UMS automáticamente."
        finally:
            k32.CloseHandle(handle)

    # 2. Fallback mediante Shell.Application (Eject verb de Windows)
    try:
        import subprocess

        ps_cmd = (
            f"$s = New-Object -ComObject Shell.Application; "
            f"$d = $s.Namespace(17).ParseName('{letter}\\'); "
            f"if ($d) {{ $d.InvokeVerb('Eject') }}"
        )
        subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps_cmd], timeout=6)
        time.sleep(0.6)
        if not Path(f"{letter}\\").exists():
            return True, f"Consola ({letter}) desconectada de forma segura."
    except Exception:
        pass

    return (
        False,
        f"No se pudo desconectar {letter} porque otra ventana tiene archivos abiertos en la SD. Cierra el Explorador e inténtalo de nuevo.",
    )


class PackBuilderEngine:
    def __init__(self):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.catalog = self.load_catalog()
        self._lock = threading.Lock()
        self.gh_sync_state: Dict[str, Any] = {
            "checking": False,
            "checked": False,
            "updated": [],
            "count": 0,
        }
        self.status: Dict[str, Any] = {
            "running": False,
            "step": "idle",
            "progress": 0,
            "message": "Conecta tu Switch por Hekate (Tools > USB Tools > SD Card) y pulsa Instalar.",
            "logs": [],
            "target_drive": None,
            "error": None,
        }

    def load_catalog(self) -> Dict[str, Any]:
        with open(INTERNAL_CATALOG_PATH, "r", encoding="utf-8") as f:
            internal_cat = json.load(f)
        if USER_CATALOG_PATH.exists():
            try:
                with open(USER_CATALOG_PATH, "r", encoding="utf-8") as f:
                    user_cat = json.load(f)
                if user_cat.get("schema_version") == internal_cat.get("schema_version"):
                    return user_cat
            except Exception:
                pass
        return internal_cat

    def save_catalog(self, data: Dict[str, Any]) -> None:
        USER_CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.catalog = data

    def log(self, msg: str, progress: Optional[int] = None, step: Optional[str] = None) -> None:
        with self._lock:
            timestamp = time.strftime("%H:%M:%S")
            entry = f"[{timestamp}] {msg}"
            self.status["logs"].append(entry)
            self.status["message"] = msg
            if progress is not None:
                self.status["progress"] = max(0, min(100, int(progress)))
            if step is not None:
                self.status["step"] = step

    def _is_cache_key_present(self, cache_key: str) -> bool:
        safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "_", cache_key)
        dest = CACHE_DIR / safe_name
        return dest.exists() and dest.stat().st_size > 0

    def _is_release_cached(self, item_id: str, install_type: str, rel: Optional[Dict[str, Any]]) -> bool:
        if not rel:
            return False
        eff_type = rel.get("install_type") or install_type
        if eff_type == "copy_multi_assets":
            assets = rel.get("assets", [])
            if not assets:
                return False
            return all(
                self._is_cache_key_present(f"{item_id}_{rel['tag']}_{a['asset_name']}")
                for a in assets
            )
        asset_name = rel.get("asset_name", "")
        if not asset_name:
            return False
        return self._is_cache_key_present(f"{item_id}_{rel['tag']}_{asset_name}")

    def resolve_for_firmware(
        self, target_fw: Optional[str] = None, base_pack_tag: Optional[str] = None
    ) -> Dict[str, Any]:
        cat = self.load_catalog()
        always_latest = cat.get("always_latest_by_default", True)

        raw_fw_releases = cat["firmware_source"]["known_releases"]
        fw_releases = (
            sorted(raw_fw_releases, key=lambda f: parse_version(f.get("version") or f.get("tag", "")), reverse=True)
            if always_latest
            else list(raw_fw_releases)
        )

        raw_base_releases = cat["base_pack_source"]["known_releases"]
        base_releases = (
            sorted(raw_base_releases, key=lambda b: parse_version(b.get("tag", "")), reverse=True)
            if always_latest
            else list(raw_base_releases)
        )

        # Si no se especificó un firmware concreto, usar siempre el último disponible
        if not target_fw or target_fw in ("latest", "auto"):
            target_fw = fw_releases[0]["version"] if fw_releases else cat.get("default_firmware", "23.0.1")

        # 1. Resolver Pack Base (Por defecto siempre el último disponible, ej. v1.19)
        selected_base = None
        if base_pack_tag and base_pack_tag not in ("auto", "latest", ""):
            for b in base_releases:
                if b["tag"] == base_pack_tag:
                    selected_base = b
                    break

        if not selected_base and base_pack_tag == "auto":
            for b in base_releases:
                if target_fw in b.get("recommended_for_fw", []):
                    selected_base = b
                    break
            if not selected_base:
                for b in base_releases:
                    if version_in_range(target_fw, b.get("min_fw", "1.0.0"), b.get("max_fw", "99.0.0")):
                        selected_base = b
                        break

        if not selected_base:
            selected_base = base_releases[0]

        selected_base = {
            **selected_base,
            "is_cached": self._is_cache_key_present(
                f"base_{selected_base['tag']}_{selected_base['asset_name']}"
            ),
        }

        atmo_ver = selected_base.get("atmosphere", "1.12.1")
        base_max_fw = selected_base.get("max_fw", "99.0.0")
        fw_incompatible = not version_in_range(target_fw, selected_base.get("min_fw", "1.0.0"), base_max_fw)
        fw_incompatibility_msg = ""
        if fw_incompatible:
            fw_incompatibility_msg = (
                f"El Pack Base {selected_base['tag']} (Atmosphere {atmo_ver}) solo soporta hasta el Firmware {base_max_fw}, "
                f"pero has seleccionado el Firmware {target_fw}. La consola no arrancará si el firmware supera al soportado por Atmosphere."
            )

        # 2. Resolver Firmware seleccionado
        selected_fw_obj = None
        for fw in fw_releases:
            if fw["version"] == target_fw or fw["tag"] == target_fw:
                selected_fw_obj = {
                    **fw,
                    "is_cached": self._is_cache_key_present(
                        f"fw_{fw['tag']}_{fw['asset_name']}"
                    ),
                }
                break
        if not selected_fw_obj and fw_releases:
            fw0 = fw_releases[0]
            target_fw = fw0["version"]
            selected_fw_obj = {
                **fw0,
                "is_cached": self._is_cache_key_present(f"fw_{fw0['tag']}_{fw0['asset_name']}"),
            }

        # 3. Resolver Apps compatibles con (target_fw, atmo_ver), ordenando siempre de MAYOR a MENOR versión
        resolved_apps = []
        for app in cat.get("apps", []):
            raw_matrix = app.get("compatibility_matrix", [])
            sorted_matrix = (
                sorted(raw_matrix, key=lambda r: parse_version(r.get("tag", "")), reverse=True)
                if always_latest
                else list(raw_matrix)
            )
            matrix = [
                {
                    **r,
                    "is_cached": self._is_release_cached(app["id"], app.get("install_type", "copy_asset"), r),
                }
                for r in sorted_matrix
            ]
            best_rel = None
            for rel in matrix:
                fw_ok = version_in_range(target_fw, rel.get("min_fw", "1.0.0"), rel.get("max_fw", "99.0.0"))
                atmo_ok = version_in_range(
                    atmo_ver, rel.get("min_atmosphere", "0.0.0"), rel.get("max_atmosphere", "99.0.0")
                )
                if fw_ok and atmo_ok:
                    best_rel = rel
                    break
            if not best_rel:
                for rel in matrix:
                    if version_in_range(target_fw, rel.get("min_fw", "1.0.0"), rel.get("max_fw", "99.0.0")):
                        best_rel = rel
                        break
            if not best_rel and matrix:
                best_rel = matrix[0]

            resolved_apps.append({
                **app,
                "compatibility_matrix": matrix,
                "resolved_release": best_rel,
                "compatible": best_rel is not None,
            })

        # 4. Resolver Payloads compatibles con target_fw, ordenando siempre de MAYOR a MENOR versión
        resolved_payloads = []
        for pl in cat.get("payloads", []):
            raw_matrix = pl.get("compatibility_matrix", [])
            sorted_matrix = (
                sorted(raw_matrix, key=lambda r: parse_version(r.get("tag", "")), reverse=True)
                if always_latest
                else list(raw_matrix)
            )
            matrix = [
                {
                    **r,
                    "is_cached": self._is_release_cached(pl["id"], pl.get("install_type", "copy_asset"), r),
                }
                for r in sorted_matrix
            ]
            best_rel = None
            for rel in matrix:
                if version_in_range(target_fw, rel.get("min_fw", "1.0.0"), rel.get("max_fw", "99.0.0")):
                    best_rel = rel
                    break
            if not best_rel and matrix:
                best_rel = matrix[0]

            resolved_payloads.append({
                **pl,
                "compatibility_matrix": matrix,
                "resolved_release": best_rel,
                "compatible": best_rel is not None,
            })

        return {
            "target_firmware": target_fw,
            "firmware_release": selected_fw_obj,
            "base_pack": selected_base,
            "atmosphere_version": atmo_ver,
            "fw_incompatible": fw_incompatible,
            "fw_incompatibility_msg": fw_incompatibility_msg,
            "apps": resolved_apps,
            "payloads": resolved_payloads,
            "all_firmwares": fw_releases,
            "all_base_packs": base_releases,
            "sd_drives": list_sd_drives(),
        }

    def _load_gh_http_cache(self) -> Dict[str, Any]:
        if GH_HTTP_CACHE_PATH.exists():
            try:
                return json.loads(GH_HTTP_CACHE_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}

    def _save_gh_http_cache(self, cache_obj: Dict[str, Any]) -> None:
        try:
            GH_HTTP_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            GH_HTTP_CACHE_PATH.write_text(json.dumps(cache_obj, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def _fetch_repo_releases_fast(
        self, repo: str, per_page: int, http_cache: Dict[str, Any], cache_lock: threading.Lock
    ) -> List[Dict[str, Any]]:
        url = f"https://api.github.com/repos/{repo}/releases?per_page={per_page}"
        headers = {"User-Agent": "TheGooniesPackBuilder/1.0", "Accept": "application/vnd.github+json"}
        with cache_lock:
            cached_entry = http_cache.get(repo, {})
        if cached_entry.get("etag"):
            headers["If-None-Match"] = cached_entry["etag"]
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 304 and cached_entry.get("data"):
                return cached_entry["data"]
            if r.status_code == 200:
                data = r.json()
                etag = r.headers.get("ETag")
                if isinstance(data, list):
                    with cache_lock:
                        http_cache[repo] = {"etag": etag, "data": data}
                    return data
            if cached_entry.get("data"):
                return cached_entry["data"]
        except Exception:
            if cached_entry.get("data"):
                return cached_entry["data"]
        return []

    def sync_with_github(self) -> Dict[str, Any]:
        cat = self.load_catalog()
        http_cache = self._load_gh_http_cache()
        cache_lock = threading.Lock()
        updated_items = []

        fw_repo = cat["firmware_source"]["repo"]
        base_repo = cat["base_pack_source"]["repo"]

        # Recopilar todos los repositorios a consultar en paralelo
        repos_to_query: List[Tuple[str, int]] = [(fw_repo, 10), (base_repo, 5)]
        for group_key in ("apps", "payloads"):
            for item in cat.get(group_key, []):
                repo = item.get("repo")
                if repo:
                    repos_to_query.append((repo, 5))

        repo_results: Dict[str, List[Dict[str, Any]]] = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
            future_map = {
                pool.submit(self._fetch_repo_releases_fast, repo, per_page, http_cache, cache_lock): repo
                for repo, per_page in repos_to_query
            }
            for fut in concurrent.futures.as_completed(future_map):
                repo_name = future_map[fut]
                try:
                    repo_results[repo_name] = fut.result()
                except Exception:
                    repo_results[repo_name] = []

        self._save_gh_http_cache(http_cache)

        # 1. Procesar Firmware
        fw_releases_gh = repo_results.get(fw_repo, [])
        if fw_releases_gh:
            known_tags = {x["tag"] for x in cat["firmware_source"]["known_releases"]}
            new_fws = []
            for rel in fw_releases_gh:
                tag = rel.get("tag_name", "")
                assets = rel.get("assets", [])
                if not assets or not tag:
                    continue
                if tag not in known_tags:
                    new_fws.append({
                        "tag": tag,
                        "version": tag.lstrip("vV"),
                        "name": f"Firmware {tag.lstrip('vV')}",
                        "asset_name": assets[0]["name"],
                        "download_url": assets[0]["browser_download_url"],
                        "size_bytes": assets[0].get("size", 0),
                    })
                    updated_items.append(f"Firmware {tag}")
            if new_fws:
                merged_fws = new_fws + cat["firmware_source"]["known_releases"]
                merged_fws.sort(key=lambda f: parse_version(f.get("version") or f.get("tag", "")), reverse=True)
                cat["firmware_source"]["known_releases"] = merged_fws
                cat["default_firmware"] = merged_fws[0]["version"]

        # 2. Procesar Pack Base (The Goonies OS)
        base_releases_gh = repo_results.get(base_repo, [])
        if base_releases_gh:
            known_tags = {x["tag"] for x in cat["base_pack_source"]["known_releases"]}
            new_bases = []
            for rel in base_releases_gh:
                tag = rel.get("tag_name", "")
                assets = rel.get("assets", [])
                if not assets or not tag or tag in known_tags:
                    continue
                title = rel.get("name", "") or tag
                body = rel.get("body", "") or ""
                atmo_match = re.search(r"atmosphere\s*v?(\d+\.\d+\.\d+)", f"{title} {body}", re.I)
                hek_match = re.search(r"hekate\s*v?(\d+\.\d+\.\d+)", f"{title} {body}", re.I)
                atmo_v = atmo_match.group(1) if atmo_match else "1.12.1"
                hek_v = hek_match.group(1) if hek_match else "6.5.4"
                latest_fw = cat["firmware_source"]["known_releases"][0]["version"]
                new_bases.append({
                    "tag": tag,
                    "name": f"The Goonies OS {tag} (Atmosphere {atmo_v} / Hekate {hek_v})",
                    "atmosphere": atmo_v,
                    "hekate": hek_v,
                    "min_fw": "1.0.0",
                    "max_fw": latest_fw,
                    "recommended_for_fw": [latest_fw],
                    "asset_name": assets[0]["name"],
                    "download_url": assets[0]["browser_download_url"],
                    "size_bytes": assets[0].get("size", 0),
                })
                updated_items.append(f"The Goonies OS {tag}")
            if new_bases:
                merged_bases = new_bases + cat["base_pack_source"]["known_releases"]
                merged_bases.sort(key=lambda b: parse_version(b.get("tag", "")), reverse=True)
                cat["base_pack_source"]["known_releases"] = merged_bases

        # 3. Procesar Aplicaciones y Payloads
        for group_key in ("apps", "payloads"):
            for item in cat.get(group_key, []):
                repo = item.get("repo")
                if not repo:
                    continue
                releases = repo_results.get(repo, [])
                if not releases:
                    continue
                non_beta = [
                    rel_item
                    for rel_item in releases
                    if not rel_item.get("draft")
                    and not re.search(r"-(alpha|beta|test)", rel_item.get("tag_name", ""), re.I)
                ]
                candidate_releases = non_beta if non_beta else releases
                releases_sorted = sorted(
                    candidate_releases, key=lambda x: parse_version(x.get("tag_name", "")), reverse=True
                )
                latest_rel = releases_sorted[0]
                tag = latest_rel.get("tag_name", "")
                existing_matrix = item.get("compatibility_matrix", [])
                known_tags = {m["tag"] for m in existing_matrix}
                max_known_ver = max((parse_version(m["tag"]) for m in existing_matrix), default=(0,))
                if tag and tag not in known_tags and parse_version(tag) >= max_known_ver:
                    entry = self._build_matrix_entry_from_gh_release(item, latest_rel)
                    if entry:
                        existing_matrix.insert(0, entry)
                        existing_matrix.sort(key=lambda m: parse_version(m.get("tag", "")), reverse=True)
                        item["compatibility_matrix"] = existing_matrix
                        updated_items.append(f"{item['name']} ({tag})")

        if updated_items:
            self.save_catalog(cat)

        with self._lock:
            self.gh_sync_state = {
                "checking": False,
                "checked": True,
                "updated": updated_items,
                "count": len(updated_items),
            }

        return {"updated": updated_items, "count": len(updated_items)}

    def start_background_github_sync(self) -> None:
        with self._lock:
            if self.gh_sync_state.get("checking"):
                return
            self.gh_sync_state["checking"] = True

        def _worker():
            try:
                self.sync_with_github()
            except Exception:
                with self._lock:
                    self.gh_sync_state["checking"] = False
                    self.gh_sync_state["checked"] = True

        threading.Thread(target=_worker, daemon=True).start()

    def _build_matrix_entry_from_gh_release(
        self, item: Dict[str, Any], gh_rel: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        tag = gh_rel.get("tag_name", "")
        assets = gh_rel.get("assets", [])
        if not assets:
            return None

        install_type = item.get("install_type", "copy_asset")
        if install_type == "copy_multi_assets":
            assets_map = item.get("assets_map", {})
            mapped_list = list(item.get("base_assets", []))
            total_sz = sum(b.get("size_bytes", 0) for b in mapped_list)
            for a in assets:
                if a["name"] in assets_map:
                    mapped_list.append({
                        "asset_name": a["name"],
                        "download_url": a["browser_download_url"],
                        "target_path": assets_map[a["name"]],
                        "size_bytes": a.get("size", 0),
                    })
                    total_sz += a.get("size", 0)
            if not mapped_list:
                return None
            return {
                "tag": tag,
                "min_fw": "1.0.0",
                "max_fw": "99.0.0",
                "assets": mapped_list,
                "size_bytes": total_sz,
            }

        pattern = item.get("asset_pattern", "*")
        matched_asset = None
        for a in assets:
            if fnmatch.fnmatch(a["name"].lower(), pattern.lower()):
                matched_asset = a
                break
        if not matched_asset and item.get("fallback_asset_pattern"):
            fb_pat = item["fallback_asset_pattern"]
            for a in assets:
                if fnmatch.fnmatch(a["name"].lower(), fb_pat.lower()):
                    matched_asset = a
                    break
        if not matched_asset:
            matched_asset = assets[0]

        return {
            "tag": tag,
            "min_fw": "1.0.0",
            "max_fw": "99.0.0",
            "asset_name": matched_asset["name"],
            "download_url": matched_asset["browser_download_url"],
            "size_bytes": matched_asset.get("size", 0),
        }

    def add_repository_item(
        self,
        item_type: str,
        name: str,
        repo_input: str,
        category: str = "Homebrew",
        description: str = "",
        default_selected: bool = True,
    ) -> Dict[str, Any]:
        repo = repo_input.strip()
        m = re.search(r"github\.com/([^/]+/[^/#?]+)", repo)
        if m:
            repo = m.group(1).rstrip("/")
            repo = re.sub(r"/releases.*$", "", repo)

        headers = {"User-Agent": "TheGooniesCreatorPack/1.0"}
        r = requests.get(f"https://api.github.com/repos/{repo}/releases?per_page=5", headers=headers, timeout=10)
        if r.status_code != 200 or not r.json():
            raise ValueError(f"No se encontraron releases públicas en el repositorio '{repo}'.")

        releases = r.json()
        latest = releases[0]
        assets = latest.get("assets", [])
        if not assets:
            raise ValueError(f"La última release ({latest.get('tag_name')}) de '{repo}' no contiene archivos adjuntos.")

        slug = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
        chosen_asset = None
        for ext in (".zip", ".nro", ".bin", ".ovl"):
            for a in assets:
                if a["name"].lower().endswith(ext):
                    chosen_asset = a
                    break
            if chosen_asset:
                break
        if not chosen_asset:
            chosen_asset = assets[0]

        a_name = chosen_asset["name"]
        lower_name = a_name.lower()

        if item_type == "payload" or lower_name.endswith(".bin"):
            group_key = "payloads"
            if lower_name.endswith(".zip"):
                install_type = "extract_zip_root"
                target_path = None
                cleanup = [f"bootloader/payloads/{slug}.bin"]
            else:
                install_type = "copy_asset"
                target_path = f"bootloader/payloads/{a_name}"
                cleanup = [target_path]
        else:
            group_key = "apps"
            if lower_name.endswith(".zip"):
                install_type = "extract_zip_root"
                target_path = None
                cleanup = [f"switch/{slug}"]
            elif lower_name.endswith(".ovl"):
                install_type = "copy_asset"
                target_path = f"switch/.overlays/{a_name}"
                cleanup = [target_path]
            else:
                install_type = "copy_asset"
                target_path = f"switch/{a_name}"
                cleanup = [target_path, f"switch/{slug}"]

        new_item: Dict[str, Any] = {
            "id": slug,
            "name": name,
            "category": category or ("Payload" if group_key == "payloads" else "Homebrew"),
            "description": description or f"Añadido desde {repo}",
            "repo": repo,
            "default_selected": default_selected,
            "included_in_base": False,
            "install_type": install_type,
            "asset_pattern": a_name,
            "cleanup_paths": cleanup,
            "compatibility_matrix": [
                {
                    "tag": latest.get("tag_name", "latest"),
                    "min_fw": "1.0.0",
                    "max_fw": "99.0.0",
                    "asset_name": a_name,
                    "download_url": chosen_asset["browser_download_url"],
                    "size_bytes": chosen_asset.get("size", 0),
                }
            ],
        }
        if target_path:
            new_item["target_path"] = target_path

        cat = self.load_catalog()
        cat[group_key] = [x for x in cat.get(group_key, []) if x["id"] != slug]
        cat[group_key].append(new_item)
        self.save_catalog(cat)
        return new_item

    def _download_file(
        self, url: str, cache_key: str, label: str, base_prog: float, span_prog: float
    ) -> Path:
        safe_name = re.sub(r"[^a-zA-Z0-9._-]+", "_", cache_key)
        dest = CACHE_DIR / safe_name
        if dest.exists() and dest.stat().st_size > 0:
            self.log(f"En caché local: {label} ({dest.name})", int(base_prog + span_prog))
            return dest

        tmp_dest = dest.with_suffix(".part")
        self.log(f"Descargando {label}...", int(base_prog))
        headers = {"User-Agent": "TheGooniesCreatorPack/1.0"}
        with requests.get(url, headers=headers, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get("Content-Length", 0))
            downloaded = 0
            last_report = 0.0
            with open(tmp_dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=256 * 1024):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if total > 0 and (now - last_report > 0.25 or downloaded == total):
                        ratio = downloaded / total
                        mb_done = downloaded / (1024 * 1024)
                        mb_tot = total / (1024 * 1024)
                        cur_p = base_prog + (span_prog * ratio)
                        self.log(
                            f"Descargando {label}: {mb_done:.1f} MB / {mb_tot:.1f} MB ({int(ratio * 100)}%)",
                            int(cur_p),
                        )
                        last_report = now

        shutil.move(str(tmp_dest), str(dest))
        return dest

    def _remove_cleanup_paths(self, sd_root: Path, rel_paths: List[str]) -> None:
        for rel_p in rel_paths:
            target = sd_root / rel_p
            if target.is_dir():
                shutil.rmtree(target, ignore_errors=True)
            elif target.exists():
                try:
                    target.unlink()
                except OSError:
                    pass

    def _validate_sd_drive(self, target_drive_str: str) -> Path:
        if not target_drive_str:
            raise ValueError("No has seleccionado ninguna unidad microSD / Consola.")
        sd_root = Path(target_drive_str).resolve()
        if not sd_root.exists():
            raise ValueError(f"La unidad {sd_root} no está conectada o no es accesible.")

        sys_drive = os.environ.get("SystemDrive", "C:").upper().rstrip("\\/")
        drive_letter = sd_root.drive.upper().rstrip("\\/")
        if not drive_letter or drive_letter == sys_drive:
            raise PermissionError(f"Operación bloqueada por seguridad: No se permite instalar en el disco del sistema ({drive_letter}).")

        if (sd_root / "Windows").exists() or (sd_root / "Program Files").exists():
            raise PermissionError("Operación bloqueada: La unidad seleccionada parece ser un disco de sistema de Windows.")

        return sd_root

    def _clean_sd_root_except_protected(self, sd_root: Path) -> None:
        """
        Borra todas las carpetas y archivos de la raíz de la microSD EXCEPTO 'emuMMC' y 'Nintendo'
        (y metadatos bloqueados de Windows como 'System Volume Information').
        """
        children = list(sd_root.iterdir())
        total = max(1, len(children))
        for idx, item in enumerate(children):
            name_lower = item.name.lower()
            if name_lower in PROTECTED_SD_ROOT_ITEMS:
                self.log(f"Protegiendo carpeta intacta: /{item.name}", progress=46 + int((idx / total) * 8))
                continue

            self.log(f"Borrando de la microSD: /{item.name}...", progress=46 + int((idx / total) * 8))
            try:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink()
            except Exception as e:
                self.log(f"Aviso al borrar /{item.name}: {e}")

    def build_pack_async(self, config: Dict[str, Any]) -> None:
        with self._lock:
            if self.status["running"]:
                raise RuntimeError("Ya hay una instalación en curso.")
            self.status = {
                "running": True,
                "step": "starting",
                "progress": 1,
                "message": "Verificando unidad microSD y preparando descargas...",
                "logs": [],
                "target_drive": config.get("target_drive"),
                "error": None,
            }
        t = threading.Thread(target=self._build_worker, args=(config,), daemon=True)
        t.start()

    def _build_worker(self, config: Dict[str, Any]) -> None:
        try:
            sd_root = self._validate_sd_drive(config.get("target_drive", ""))
            target_fw = config.get("target_firmware", self.catalog.get("default_firmware", "23.0.1"))
            include_fw_files = config.get("include_firmware_files", True)
            base_pack_tag = config.get("base_pack_tag", "v1.18")
            selected_app_ids = set(config.get("selected_apps", []))
            selected_payload_ids = set(config.get("selected_payloads", []))
            custom_versions = config.get("custom_versions", {})

            resolved = self.resolve_for_firmware(target_fw, base_pack_tag)
            base_pack = resolved["base_pack"]
            fw_release = resolved["firmware_release"]
            apps = resolved["apps"]
            payloads = resolved["payloads"]

            self.log(
                f"Unidad destino: {sd_root} | Pack Base: {base_pack['tag']} | Firmware: {target_fw}",
                progress=3,
                step="downloading",
            )

            # =========================================================================
            # FASE 1: DESCARGAR TODO EN CACHÉ ANTES DE TOCAR LA MICROSD (3% -> 45%)
            # =========================================================================
            base_zip_path = self._download_file(
                base_pack["download_url"],
                f"base_{base_pack['tag']}_{base_pack['asset_name']}",
                f"Pack Base ({base_pack['tag']})",
                base_prog=3,
                span_prog=14,
            )

            # Pre-descargar Apps seleccionadas (17% -> 28%)
            active_apps_to_install: List[Tuple[Dict[str, Any], Dict[str, Any], List[Tuple[Path, Optional[str]]]]] = []
            sel_apps_list = [a for a in apps if a["id"] in selected_app_ids]
            for idx, app in enumerate(sel_apps_list):
                b_p = 17 + (idx / max(1, len(sel_apps_list))) * 11
                s_p = 11 / max(1, len(sel_apps_list))
                rel = app["resolved_release"]
                override_tag = custom_versions.get(app["id"])
                if override_tag:
                    for m in app.get("compatibility_matrix", []):
                        if m["tag"] == override_tag:
                            rel = m
                            break
                if not rel:
                    continue
                downloaded_files = self._predownload_item_files(app, rel, b_p, s_p)
                active_apps_to_install.append((app, rel, downloaded_files))

            # Pre-descargar Payloads seleccionados (28% -> 32%)
            active_pls_to_install: List[Tuple[Dict[str, Any], Dict[str, Any], List[Tuple[Path, Optional[str]]]]] = []
            sel_pls_list = [p for p in payloads if p["id"] in selected_payload_ids]
            for idx, pl in enumerate(sel_pls_list):
                b_p = 28 + (idx / max(1, len(sel_pls_list))) * 4
                s_p = 4 / max(1, len(sel_pls_list))
                rel = pl["resolved_release"]
                override_tag = custom_versions.get(pl["id"])
                if override_tag:
                    for m in pl.get("compatibility_matrix", []):
                        if m["tag"] == override_tag:
                            rel = m
                            break
                if not rel:
                    continue
                downloaded_files = self._predownload_item_files(pl, rel, b_p, s_p)
                active_pls_to_install.append((pl, rel, downloaded_files))

            # Pre-descargar Firmware si está marcado (32% -> 45%)
            fw_zip_path: Optional[Path] = None
            if include_fw_files and fw_release:
                fw_zip_path = self._download_file(
                    fw_release["download_url"],
                    f"fw_{fw_release['tag']}_{fw_release['asset_name']}",
                    f"Firmware {fw_release['version']}",
                    base_prog=32,
                    span_prog=13,
                )

            # Verificar que la consola sigue conectada antes de limpiar
            if not sd_root.exists():
                raise RuntimeError(f"La unidad {sd_root} se ha desconectado antes de iniciar la instalación.")

            # =========================================================================
            # FASE 2: LIMPIAR RAÍZ DE MICROSD EXCEPTO emuMMC Y Nintendo (45% -> 55%)
            # =========================================================================
            self.log(
                f"Limpiando raíz de {sd_root} (conservando intactas 'emuMMC' y 'Nintendo')...",
                progress=45,
                step="cleaning_sd",
            )
            self._clean_sd_root_except_protected(sd_root)

            # =========================================================================
            # FASE 3: EXTRAER PACK BASE DIRECTAMENTE EN LA MICROSD (55% -> 72%)
            # =========================================================================
            self.log(f"Instalando Pack Base {base_pack['tag']} en {sd_root}...", progress=55, step="extracting_base")
            with zipfile.ZipFile(base_zip_path, "r") as zf:
                members = zf.infolist()
                tot_m = max(1, len(members))
                for i, member in enumerate(members):
                    # Ignorar cualquier carpeta "Firmware*" que pudiera venir dentro de un pack antiguo
                    if member.filename.lower().startswith("firmware"):
                        continue
                    zf.extract(member, sd_root)
                    if i % 25 == 0 or i == tot_m - 1:
                        pct = 55 + int(((i + 1) / tot_m) * 17)
                        self.log(
                            f"Copiando archivos del Pack Base a la SD ({i + 1}/{tot_m})...",
                            progress=pct,
                            step="extracting_base",
                        )

            # =========================================================================
            # FASE 4: APLICAR APPS Y PAYLOADS (Y BORRAR DESMARCADOS DEL BASE) (72% -> 84%)
            # =========================================================================
            for app in apps:
                if app["id"] not in selected_app_ids and app.get("cleanup_paths"):
                    self._remove_cleanup_paths(sd_root, app["cleanup_paths"])
                    if app.get("included_in_base"):
                        self.log(f"Eliminada del pack base (desmarcada): {app['name']}", progress=74, step="apps")

            for idx, (app, rel, dl_files) in enumerate(active_apps_to_install):
                pct = 74 + int(((idx + 1) / max(1, len(active_apps_to_install))) * 7)
                self._apply_downloaded_item_to_sd(sd_root, app, rel, dl_files, pct)

            for pl in payloads:
                if pl["id"] not in selected_payload_ids and pl.get("cleanup_paths"):
                    self._remove_cleanup_paths(sd_root, pl["cleanup_paths"])
                    if pl.get("included_in_base"):
                        self.log(f"Payload eliminado del base (desmarcado): {pl['name']}", progress=81, step="payloads")

            for idx, (pl, rel, dl_files) in enumerate(active_pls_to_install):
                pct = 81 + int(((idx + 1) / max(1, len(active_pls_to_install))) * 3)
                self._apply_downloaded_item_to_sd(sd_root, pl, rel, dl_files, pct)

            # =========================================================================
            # FASE 5: EXTRAER FIRMWARE EN /Firmware X.Y.Z/ EN LA MICROSD (84% -> 98%)
            # =========================================================================
            if include_fw_files and fw_release and fw_zip_path:
                fw_folder_name = f"Firmware {fw_release['version']}"
                fw_target_dir = sd_root / fw_folder_name
                fw_target_dir.mkdir(parents=True, exist_ok=True)
                self.log(f"Copiando {fw_folder_name} en la microSD para Daybreak...", progress=85, step="firmware")
                with zipfile.ZipFile(fw_zip_path, "r") as zf:
                    nca_members = [m for m in zf.infolist() if not m.is_dir()]
                    tot_nca = max(1, len(nca_members))
                    for i, member in enumerate(nca_members):
                        filename = Path(member.filename).name
                        if not filename or filename.startswith("."):
                            continue
                        dest_file = fw_target_dir / filename
                        with zf.open(member) as src, open(dest_file, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                        if i % 15 == 0 or i == tot_nca - 1:
                            pct = 85 + int(((i + 1) / tot_nca) * 13)
                            self.log(
                                f"Copiando archivos de {fw_folder_name} ({i + 1}/{tot_nca})...",
                                progress=pct,
                                step="firmware",
                            )

            # =========================================================================
            # FASE 6: RESUMEN Y CIERRE SEGURO (98% -> 100%)
            # =========================================================================
            self._write_pack_manifest(
                sd_root,
                target_fw=target_fw,
                include_fw_files=include_fw_files,
                base_pack=base_pack,
                apps=[a for a in apps if a["id"] in selected_app_ids],
                payloads=[p for p in payloads if p["id"] in selected_payload_ids],
            )

            with self._lock:
                self.status["running"] = False
            self.log(
                f'¡Instalación completada en {sd_root}! Ya puedes desconectar la consola desde el botón "Desconectar consola" o desde "Quitar hardware de forma segura" en la barra de tareas de Windows.',
                progress=100,
                step="completed",
            )

        except Exception as e:
            with self._lock:
                self.status["error"] = str(e)
                self.status["running"] = False
            self.log(f"Error durante la instalación: {e}", step="error")

    def _predownload_item_files(
        self, item: Dict[str, Any], rel: Dict[str, Any], base_prog: float, span_prog: float
    ) -> List[Tuple[Path, Optional[str]]]:
        install_type = rel.get("install_type") or item.get("install_type", "copy_asset")
        item_name = f"{item['name']} ({rel['tag']})"
        results: List[Tuple[Path, Optional[str]]] = []

        if install_type == "copy_multi_assets":
            assets = rel.get("assets", [])
            sub_span = span_prog / max(1, len(assets))
            for i, asset in enumerate(assets):
                f_path = self._download_file(
                    asset["download_url"],
                    f"{item['id']}_{rel['tag']}_{asset['asset_name']}",
                    f"{item_name} - {asset['asset_name']}",
                    base_prog + i * sub_span,
                    sub_span,
                )
                results.append((f_path, asset["target_path"]))
            return results

        f_path = self._download_file(
            rel["download_url"],
            f"{item['id']}_{rel['tag']}_{rel['asset_name']}",
            item_name,
            base_prog,
            span_prog,
        )
        target_rel = rel.get("target_path") or item.get("target_path")
        results.append((f_path, target_rel))
        return results

    def _apply_downloaded_item_to_sd(
        self,
        sd_root: Path,
        item: Dict[str, Any],
        rel: Dict[str, Any],
        dl_files: List[Tuple[Path, Optional[str]]],
        pct: int,
    ) -> None:
        install_type = rel.get("install_type") or item.get("install_type", "copy_asset")
        item_name = f"{item['name']} ({rel['tag']})"

        if install_type != "copy_asset_preserve_dir" and item.get("cleanup_paths"):
            self._remove_cleanup_paths(sd_root, item["cleanup_paths"])

        if install_type == "copy_multi_assets":
            for f_path, target_rel in dl_files:
                if not target_rel:
                    continue
                if target_rel.startswith("@extract:"):
                    sub_dir = target_rel.split(":", 1)[1].strip("/")
                    extract_dest = sd_root / sub_dir if sub_dir and sub_dir != "." else sd_root
                    extract_dest.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(f_path, "r") as zf:
                        zf.extractall(extract_dest)
                else:
                    dest = sd_root / target_rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f_path, dest)
            self.log(f"Instalado en microSD: {item_name}", progress=pct, step="apps")
            return

        f_path, target_rel = dl_files[0]
        if install_type == "extract_zip_root":
            with zipfile.ZipFile(f_path, "r") as zf:
                zf.extractall(sd_root)
        elif install_type in ("copy_asset", "copy_asset_preserve_dir"):
            if not target_rel:
                target_rel = f"switch/{rel['asset_name']}"
            dest = sd_root / target_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f_path, dest)

        self.log(f"Instalado en microSD: {item_name}", progress=pct, step="apps")

    def _write_pack_manifest(
        self,
        sd_root: Path,
        target_fw: str,
        include_fw_files: bool,
        base_pack: Dict[str, Any],
        apps: List[Dict[str, Any]],
        payloads: List[Dict[str, Any]],
    ) -> None:
        lines = [
            "==============================================================",
            "             THE GOONIES PACK BUILDER - INSTALADO             ",
            "==============================================================",
            f"Fecha de instalación : {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Pack CFW Base        : {base_pack['name']} ({base_pack['tag']})",
            f"Atmosphere           : v{base_pack.get('atmosphere', 'N/A')}",
            f"Hekate               : v{base_pack.get('hekate', 'N/A')}",
            f"Firmware Objetivo    : {target_fw}",
            f"Carpeta Firmware     : {'Incluida (/Firmware ' + target_fw + ')' if include_fw_files else 'No incluida'}",
            "",
            "--- APLICACIONES INSTALADAS ---",
        ]
        if apps:
            for a in apps:
                ver = a["resolved_release"]["tag"] if a.get("resolved_release") else "N/A"
                lines.append(f" [x] {a['name']} (Versión: {ver})")
        else:
            lines.append(" (Ninguna aplicación extra seleccionada)")

        lines.append("")
        lines.append("--- PAYLOADS INSTALADOS ---")
        if payloads:
            for p in payloads:
                ver = p["resolved_release"]["tag"] if p.get("resolved_release") else "N/A"
                lines.append(f" [x] {p['name']} (Versión: {ver})")
        else:
            lines.append(" (Solo fusee.bin del sistema base)")

        lines.append("==============================================================")
        (sd_root / "GOONIES_PACK_INFO.txt").write_text("\n".join(lines), encoding="utf-8")
