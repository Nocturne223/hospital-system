@echo off
echo ========================================
echo Hospital Management System
echo Starting Streamlit Application...
echo ========================================
echo.
cd /d "%~dp0"
python -m streamlit run app.py
if errorlevel 1 (
    echo.
    echo Application exited with error code: %errorlevel%
    echo.
    pause
)
