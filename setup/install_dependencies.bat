@echo off
echo [INFO] Installing Claude Capture Dependencies
echo =======================================
echo.

REM Simple dependency installation
echo [INFO] Installing watchdog...
pip install watchdog

echo.
echo [INFO] Installing psutil...
pip install psutil

echo.
echo [INFO] Testing imports...
python -c "import watchdog; import psutil; print('All dependencies installed successfully!')"

echo.
echo [SUCCESS] Dependencies installed! Now try: .\claude_start.bat
echo.
pause