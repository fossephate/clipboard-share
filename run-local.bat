@echo off
:loop
python -m pipenv run python main.py W:\clip.txt
if %ERRORLEVEL% neq 0 (
    echo Script crashed with exit code %ERRORLEVEL%. Restarting...
    timeout /t 5
    goto loop
)