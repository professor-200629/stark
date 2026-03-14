@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    STARK AI ASSISTANT                         ║
echo ║                   Starting up...                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

:: Change to script directory
cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please run INSTALL_STARK.bat first.
    pause
    exit /b 1
)

:: Check if virtual environment exists, create if not
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run STARK
echo [INFO] Starting STARK...
echo.
python main.py

:: Deactivate on exit
call venv\Scripts\deactivate.bat

pause
