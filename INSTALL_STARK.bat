@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║               STARK AI ASSISTANT - INSTALLER                  ║
echo ║                  Setting up your environment                  ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please download Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [✓] Python detected
echo.

:: Install/upgrade pip
echo [1/4] Upgrading pip...
python -m pip install --upgrade pip

:: Install PyAudio using pipwin (Windows-specific)
echo [2/4] Installing PyAudio (Windows)...
pip install pipwin
pipwin install pyaudio

:: Install all requirements
echo [3/4] Installing all dependencies...
cd /d "%~dp0"
pip install -r requirements.txt

echo [4/4] Installing additional packages...
pip install pywhatkit screen-brightness-control

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    INSTALLATION COMPLETE!                       ║
echo ║                                                                 ║
echo ║  To run STARK:                                                  ║
echo ║     1. Double-click RUN_STARK.bat                              ║
echo ║     2. Or run: python main.py                                    ║
echo ║                                                                 ║
echo ║  IMPORTANT: Install Tesseract OCR for screen reading:            ║
echo ║     https://github.com/UB-Mannheim/tesseract/wiki              ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
pause
