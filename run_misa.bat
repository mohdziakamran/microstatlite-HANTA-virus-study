@ECHO OFF
@REM if not exist .venv\ (
@REM     python -m pip venv .venv
@REM )
@REM cd .venv\Scripts
@REM activate.bat
@REM cd ../..
@REM PAUSE
cd src/misa_extraction
..\..\.venv\Scripts\python misa_exteact.py
PAUSE