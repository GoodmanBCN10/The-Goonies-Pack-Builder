@echo off
title Compilar The Goonies Pack Builder (.EXE)
cd /d "%~dp0"
taskkill /F /IM TheGooniesPackBuilder.exe >nul 2>&1
taskkill /F /IM TheGooniesCreatorPack.exe >nul 2>&1
echo Compilando The Goonies Pack Builder en un unico archivo ejecutable (.exe)...
python -m PyInstaller --noconfirm --onefile --windowed --icon "static/logo.ico" --name "TheGooniesPackBuilder" --add-data "static;static" --add-data "catalog.json;." app.py
echo.
echo Compilacion finalizada. El ejecutable listo para compartir se encuentra en:
echo dist\TheGooniesPackBuilder.exe
pause
