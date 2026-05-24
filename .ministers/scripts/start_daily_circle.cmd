@echo off
set LOG=C:\Users\ashershih\Documents\alchplan\alchplan-data\daily_circle.log

echo [%DATE% %TIME%] Starting daily circle... >> "%LOG%" 2>&1

wsl.exe -d Ubuntu -- bash -c "cd /mnt/c/Users/ashershih/Documents/alchplan/alchplan-data && python3 .ministers/run.py all >> /mnt/c/Users/ashershih/Documents/alchplan/alchplan-data/daily_circle.log 2>&1"

echo [%DATE% %TIME%] Daily circle finished. >> "%LOG%" 2>&1
