@echo off
title Django Developer Portfolio Server
cd /d "%~dp0"
echo Starting Django development server at http://127.0.0.1:8000 ...
".venv\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
pause
