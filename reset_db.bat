@echo off
cd /d %~dp0
if exist db.sqlite3 del /f /q db.sqlite3
if exist db.sqlite3-journal del /f /q db.sqlite3-journal

python manage.py migrate
if errorlevel 1 (
    echo Migration failed.
    exit /b 1
)
python manage.py loaddata initial_data.json
if errorlevel 1 (
    echo loaddata failed.
    exit /b 1
)
echo Reset complete. Database has been rebuilt and seeded.
