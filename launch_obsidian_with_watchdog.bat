@echo off

REM WHERE IS YOUR PROJECT LOCATED?
set "PROJECT_PATH=%~dp0"

REM GET THE PATH TO OBSIDIAN.EXE
set "OBSIDIAN_PATH=%LOCALAPPDATA%\Obsidian\Obsidian.exe"

set "VENV_PATH=%PROJECT_PATH%env\Scripts\activate.bat"
set "MAIN_PY=%PROJECT_PATH%main.py"

REM Activate the virtual environment and run the Python script
start cmd.exe /k "call ""%VENV_PATH%"" && cd /d ""%PROJECT_PATH%"" && python ""%MAIN_PY%"""

REM Launch Obsidian
start "" "%OBSIDIAN_PATH%"
