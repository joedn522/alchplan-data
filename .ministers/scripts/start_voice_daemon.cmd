@echo off
set PY=C:\Users\ashershih\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPT=C:\Users\ashershih\Documents\alchplan\alchplan-data\.ministers\scripts\voice_daemon.py
set LOG=C:\Users\ashershih\Documents\alchplan\alchplan-data\voice_daemon.log

"%PY%" "%SCRIPT%" >> "%LOG%" 2>&1
