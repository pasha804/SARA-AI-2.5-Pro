@echo off
title SARA AI — Clean Reinstall & Diagnostics Utility
echo ========================================================
echo        SARA AI — CLEAN RESET & REINSTALL UTILITY
echo ========================================================
echo.
echo 1. Stopping any active SARA/MYRAA processes...
taskkill /F /IM SARA.exe 2>nul
taskkill /F /IM MYRAA.exe 2>nul
taskkill /F /IM myraa-agent.exe 2>nul
echo Processes cleanly stopped.
echo.

echo 2. Available Options:
echo    [1] Launch SARA Now
echo    [2] Clean Cache & Relaunch SARA
echo    [3] Run Full Uninstaller (Uninstall SARA / MYRAA)
echo    [4] Re-run Setup from MYRAA-Setup-1.0.1.exe
echo.
set /p choice="Enter option (1-4): "

if "%choice%"=="1" (
    echo Launching SARA...
    start "" "d:\MARAA AI\MYRAA\SARA.exe"
    exit
)
if "%choice%"=="2" (
    echo Clearing temporary caches...
    del /q /f "%TEMP%\myraa-screen-share-smoke.json" 2>nul
    echo Relaunching SARA...
    start "" "d:\MARAA AI\MYRAA\SARA.exe"
    exit
)
if "%choice%"=="3" (
    echo Launching uninstaller...
    start "" "d:\MARAA AI\MYRAA\Uninstall SARA.exe"
    exit
)
if "%choice%"=="4" (
    echo Running installer...
    start "" "d:\MARAA AI\MYRAA-Setup-1.0.1.exe"
    exit
)

echo Invalid choice. Exiting.
pause
