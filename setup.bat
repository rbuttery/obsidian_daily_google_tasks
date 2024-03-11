@echo off

REM Set the path to the project
set "PROJECT_PATH=C:\Projects\obsidian_launcher"

REM Set the full path to the virtual environment
set "VENV_PATH=%PROJECT_PATH%\env"

REM Check if the virtual environment directory exists
if not exist "%VENV_PATH%" (
    REM The directory doesn't exist, so create the virtual environment
    python -m venv "%VENV_PATH%"
    echo Virtual environment created at %VENV_PATH%
) else (
    echo Virtual environment already exists at %VENV_PATH%
)

REM Activate the virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

REM Install dependencies from requirements.txt
pip install -r "%PROJECT_PATH%\requirements.txt"

echo Dependencies installed.
pause
