@echo off
REM 安裝 AlchPlan 每日 Circle — 每天早上 8:00 自動跑所有部長
set WRAPPER=C:\Users\ashershih\Documents\alchplan-data\.ministers\scripts\start_daily_circle.cmd

schtasks /Create ^
  /TN "AlchPlan Daily Circle" ^
  /TR "\"%WRAPPER%\"" ^
  /SC DAILY ^
  /ST 08:00 ^
  /RU "%USERNAME%" ^
  /RL LIMITED ^
  /F

if %ERRORLEVEL% == 0 (
    echo [OK] Task created. Circle will run daily at 08:00.
    echo To run immediately: schtasks /Run /TN "AlchPlan Daily Circle"
) else (
    echo [FAIL] Could not create task. Try running as Administrator.
)
pause
