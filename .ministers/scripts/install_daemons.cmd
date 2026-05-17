@echo off
REM 一次安裝 Voice Daemon + Obsidian Audio Daemon
REM 以一般使用者執行即可（不需要 admin）

set PY=C:\Users\ashershih\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPTS=C:\Users\ashershih\Documents\alchplan-data\.ministers\scripts
set LOG_DIR=C:\Users\ashershih\Documents\alchplan-data

echo === 安裝 Voice Daemon ===
schtasks /Create ^
  /TN "AlchPlan Voice Daemon" ^
  /TR "\"%PY%\" \"%SCRIPTS%\voice_daemon.py\" >> \"%LOG_DIR%\voice_daemon.log\" 2>&1" ^
  /SC ONLOGON /RU "%USERNAME%" /RL LIMITED /F
if %ERRORLEVEL% == 0 (echo [OK] Voice Daemon 已安裝) else (echo [FAIL] Voice Daemon 安裝失敗)

echo.
echo === 安裝 Obsidian Audio Daemon ===
schtasks /Create ^
  /TN "AlchPlan Obsidian Daemon" ^
  /TR "\"%PY%\" \"%SCRIPTS%\obsidian_audio_daemon.py\" >> \"%LOG_DIR%\obsidian_daemon.log\" 2>&1" ^
  /SC ONLOGON /RU "%USERNAME%" /RL LIMITED /F
if %ERRORLEVEL% == 0 (echo [OK] Obsidian Daemon 已安裝) else (echo [FAIL] Obsidian Daemon 安裝失敗)

echo.
echo === 現在啟動兩個 Daemon ===
schtasks /Run /TN "AlchPlan Voice Daemon"
schtasks /Run /TN "AlchPlan Obsidian Daemon"

echo.
echo 完成！兩個 daemon 現在在背景運作中。
echo Log 位置：
echo   Voice:    %LOG_DIR%\voice_daemon.log
echo   Obsidian: %LOG_DIR%\obsidian_daemon.log
pause
