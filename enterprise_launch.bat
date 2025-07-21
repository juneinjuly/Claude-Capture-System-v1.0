@echo off
echo.
echo ===============================================
echo  Enterprise Intelligence System Launcher
echo ===============================================
echo.

echo [INFO] Testing Enterprise Intelligence System...
echo.

REM Try different Python commands
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Using 'python' command
    python tests\test_enterprise_system.py
    goto :end
)

where python3 >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Using 'python3' command
    python3 tests\test_enterprise_system.py
    goto :end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Using 'py' command
    py tests\test_enterprise_system.py
    goto :end
)

echo [ERROR] Python not found! Please install Python 3.x
echo [INFO] Download from: https://python.org/downloads/
echo.
pause

:end
echo.
echo [INFO] Enterprise Intelligence System test complete.
echo.
pause