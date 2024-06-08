@echo off
set ORIGIN=%CD%
cd /d %~dp0
call .venv\Scripts\activate.bat
python src\script.py %*
cd /d %ORIGIN%
deactivate
