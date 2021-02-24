@echo off
echo Starting setup...

echo Installing virtual environment...

python -m venv venv

echo Installing packages...

%cd%\venv\Scripts\pip install -r requirements.txt

echo Imported required packages.

python bot.py

echo Done, process finished, your bot should now be online.

PAUSE
