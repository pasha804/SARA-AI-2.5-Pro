@echo off
title SARA AI — Launching Desktop Companion
echo ========================================================
echo        STARTING SARA AI (PASHA DEV EDITION)
echo ========================================================
echo.

cd /d "D:\MARAA AI\SARA"

echo [1/3] Stopping any previous hanging instances...
taskkill /F /IM SARA.exe 2>nul
taskkill /F /IM MYRAA-runtime.exe 2>nul
taskkill /F /IM MYRAA.exe 2>nul
taskkill /F /IM myraa-agent.exe 2>nul

echo [2/3] Verified port 3344 dedicated for SARA (Port 3000 reserved for MUBAR store).
echo [3/3] Starting SARA Desktop Companion...
start "" "D:\MARAA AI\SARA\MYRAA.exe"

echo.
echo SARA is launched successfully!
ping 127.0.0.1 -n 3 >nul
exit
