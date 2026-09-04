@echo off
REM Run EventBuzz – use from the eventbuzz folder (where manage.py is)
cd /d "%~dp0"

REM Activate venv if it exists here
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Or activate venv in parent folder (Aict project\venv)
if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
)

echo Applying migrations...
python manage.py migrate
echo.
echo Starting server at http://127.0.0.1:8000/
python manage.py runserver
pause
