@echo off
REM 安裝 Voice Daemon（Obsidian Audio Daemon 已退役,不再安裝）
REM 以一般使用者執行即可（不需要 admin）

set PY=C:\Users\ashershih\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPTS=C:\Users\ashershih\Documents\alchplan\alchplan-data\.ministers\scripts
set LOG_DIR=C:\Users\ashershih\Documents\alchplan\alchplan-data

echo === 安裝 Voice Daemon ===
schtasks /Create ^
  /TN "AlchPlan Voice Daemon" ^
  /TR "\"%PY%\" \"%SCRIPTS%\voice_daemon.py\" >> \"%LOG_DIR%\voice_daemon.log\" 2>&1" ^
  /SC ONLOGON /RU "%USERNAME%" /RL LIMITED /F
if %ERRORLEVEL% == 0 (echo [OK] Voice Daemon 已安裝) else (echo [FAIL] Voice Daemon 安裝失敗)

echo.
echo === 現在啟動 Daemon ===
schtasks /Run /TN "AlchPlan Voice Daemon"

echo.
echo 完成！Voice daemon 現在在背景運作中。（Obsidian daemon 已退役）
echo Log 位置：
echo   Voice:    %LOG_DIR%\voice_daemon.log
pause
