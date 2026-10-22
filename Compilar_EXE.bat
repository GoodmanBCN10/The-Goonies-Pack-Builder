@echo off
chcp 65001 >nul
title Compilando The Goonies Pack Builder (.EXE)
echo ===================================================
echo   Compilando TheGooniesPackBuilder.exe ...
echo ===================================================
cd /d "%~dp0"
python -m PyInstaller --noconfirm --onefile --windowed --icon "static/logo.ico" --version-file "version_info.txt" --name "TheGooniesPackBuilder" --add-data "static;static" --add-data "catalog.json;." app.py
echo.
echo ===================================================
echo   Compilacion completada!
echo   Ejecutable listo en: dist\TheGooniesPackBuilder.exe
echo ===================================================
pause
