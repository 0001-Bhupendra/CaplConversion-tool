@echo off
REM ============================================================================
REM  TXT to CAPL Converter Tool - Launch Script
REM ============================================================================
REM
REM  This script starts the Streamlit web application.
REM  The app opens automatically in your default browser.
REM
REM  Requirements:
REM  • Python 3.8+ installed
REM  • Streamlit installed (pip install streamlit)
REM
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                  TXT to CAPL Converter Tool                            ║
echo ║                                                                        ║
echo ║            Converting test cases to CAPL modules...                   ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if Streamlit is installed
python -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo WARNING: Streamlit not found. Installing now...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Please run: python -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo ✓ Dependencies verified
echo.
echo ════════════════════════════════════════════════════════════════════════
echo Starting web application...
echo.
echo The app will open in your default browser at: http://localhost:8501
echo.
echo To stop the application, close this window or press Ctrl+C
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Start the application
python -m streamlit run app.py

pause
