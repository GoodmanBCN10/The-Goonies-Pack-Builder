@echo off
chcp 65001 >nul
title Compilando The Goonies Pack Builder (HERMETICO .EXE)
echo ===================================================
echo   Compilando TheGooniesPackBuilder.exe (Blindado)
echo ===================================================
cd /d "%~dp0"
python build_hermetic.py
echo.
pause
