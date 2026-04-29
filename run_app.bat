@echo off
echo Starting Name Duplicate Detector in single window...

:: Activate Virtual Environment and run the Python orchestrator
call .venv\Scripts\activate
python run_servers.py

pause