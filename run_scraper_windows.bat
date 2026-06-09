@echo off
cd /d "%~dp0"
python scrapeKeyTerms.py %1
pause