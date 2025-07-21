@echo off
echo [INFO] Claude Capture System - Windows Test
echo ====================================
echo.

REM Run the Windows-compatible test
python claude_capture\tests\test_capture_windows_simple.py

echo.
echo [INFO] Test complete!
echo.
pause