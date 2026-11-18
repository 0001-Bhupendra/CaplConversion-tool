# ============================================================================
#  TXT to CAPL Converter Tool - PowerShell Launch Script
# ============================================================================
#
#  Usage: .\run_tool.ps1
#
#  This script starts the Streamlit web application.
#  The app opens automatically in your default browser.
#
# ============================================================================

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                  TXT to CAPL Converter Tool                            ║" -ForegroundColor Cyan
Write-Host "║                                                                        ║" -ForegroundColor Cyan
Write-Host "║            Converting test cases to CAPL modules...                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Streamlit is installed
Write-Host ""
$streamlitCheck = python -m pip show streamlit 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "WARNING: Streamlit not found. Installing now..." -ForegroundColor Yellow
    Write-Host ""
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Write-Host "Please run: python -m pip install -r requirements.txt" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "✓ Dependencies verified" -ForegroundColor Green
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Starting web application..." -ForegroundColor Cyan
Write-Host ""
Write-Host "The app will open in your default browser at: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop the application, close this window or press Ctrl+C" -ForegroundColor Yellow
Write-Host "════════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Start the application
python -m streamlit run app.py

Read-Host "Press Enter to exit"
