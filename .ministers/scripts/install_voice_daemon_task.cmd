@echo off
REM Run this once as normal user (no admin needed for ONLOGON + current user)
set WRAPPER=C:\Users\ashershih\Documents\alchplan\alchplan-data\.ministers\scripts\start_voice_daemon.cmd

schtasks /Create ^
  /TN "AlchPlan Voice Daemon" ^
  /TR "\"%WRAPPER%\"" ^
  /SC ONLOGON ^
  /RU "%USERNAME%" ^
  /RL LIMITED ^
  /F

if %ERRORLEVEL% == 0 (
    echo [OK] Task created. Daemon will start on next login.
    echo Starting now...
    schtasks /Run /TN "AlchPlan Voice Daemon"
) else (
    echo [FAIL] Could not create task. Try running as Administrator.
)
pause
