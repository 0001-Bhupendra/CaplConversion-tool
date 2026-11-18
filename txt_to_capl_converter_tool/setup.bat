@echo off
REM ============================================================================
REM  TXT to CAPL Converter Tool - Setup Script
REM ============================================================================
REM
REM  This script sets up the Python environment and installs dependencies.
REM  Run this once before first use.
REM
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║          TXT to CAPL Converter Tool - Setup Wizard                     ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please download and install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo During installation:
    echo   1. CHECK the box "Add Python to PATH"
    echo   2. Choose "Install for all users" (optional)
    echo   3. Complete the installation
    echo   4. Run this setup script again
    echo.
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version
echo.

REM Create virtual environment (optional)
set /p useVenv="Do you want to create a virtual environment? (y/n): "
if /i "%useVenv%"=="y" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment created and activated
    echo.
)

REM Install dependencies
echo Installing Python packages...
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Try running manually:
    echo   python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Dependencies installed successfully
echo.

REM Verify installation
echo Verifying installation...
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo WARNING: Streamlit verification failed
    echo But installation appears to have completed
    echo.
)

echo.
echo ════════════════════════════════════════════════════════════════════════
echo ✓ Setup Complete!
echo ════════════════════════════════════════════════════════════════════════
echo.
echo Next steps:
echo   1. Run: run_tool.bat
echo   2. Or: streamlit run app.py
echo   3. Browser opens to: http://localhost:8501
echo.
echo For detailed instructions, see: QUICKSTART.txt
echo.
pause
