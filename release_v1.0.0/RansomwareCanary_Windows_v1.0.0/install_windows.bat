@echo off
REM Ransomware Canary - Windows Installation Script
REM This script creates a Start Menu shortcut and auto-start entry
REM Run as Administrator for full installation

echo =====================================================
echo Ransomware Canary - Windows Installer
echo =====================================================
echo.

REM Get the current directory
set APP_DIR=%~dp0
set APP_DIR=%APP_DIR:~0,-1%

REM Check if executable exists
if not exist "%APP_DIR%\dist\RansomwareCanary.exe" (
    echo [-] ERROR: RansomwareCanary.exe not found in dist\ folder!
    echo [-] Please build the executable first using PyInstaller.
    pause
    exit /b 1
)

echo [*] Installing Ransomware Canary...
echo.

REM Get user's AppData directory
set USER_PROFILE=%USERPROFILE%
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM Create Start Menu shortcut
echo [*] Creating Start Menu shortcut...
mkdir "%START_MENU%\RansomwareCanary" 2>nul

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\RansomwareCanary\Ransomware Canary.lnk'); $Shortcut.TargetPath = '%APP_DIR%\dist\RansomwareCanary.exe'; $Shortcut.WorkingDirectory = '%APP_DIR%\dist'; $Shortcut.Description = 'Active Defense System - Zero-Infrastructure Endpoint Protection'; $Shortcut.Save()"

REM Create auto-start shortcut
echo [*] Adding to Startup folder...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTUP%\RansomwareCanary.lnk'); $Shortcut.TargetPath = '%APP_DIR%\dist\RansomwareCanary.exe'; $Shortcut.WorkingDirectory = '%APP_DIR%\dist'; $Shortcut.Description = 'Ransomware Canary - Auto-start'; $Shortcut.Save()"

echo.
echo =====================================================
echo [+] INSTALLATION COMPLETE.
echo.
echo The app has been added to:
echo   1. Start Menu: Press Windows key, search "Ransomware Canary"
echo   2. Startup: Will auto-start on every boot
echo.
echo To test: Reboot your computer or launch from Start Menu.
echo =====================================================
echo.
pause

