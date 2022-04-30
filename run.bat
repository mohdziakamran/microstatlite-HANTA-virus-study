@ECHO OFF
@REM if not exist .venv\ (
@REM     python -m pip venv .venv
@REM )
@REM cd .venv\Scripts
@REM activate.bat
@REM cd ../..
@REM PAUSE
.venv\Scripts\python main.py
PAUSE