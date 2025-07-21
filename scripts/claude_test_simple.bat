@echo off
echo [INFO] Claude Capture System - Simple Test
echo ===================================
echo.

REM Run the Windows-compatible test from project root
python claude_capture\tests\test_capture_windows_simple.py

echo.
echo [INFO] Test complete!
echo.
pause