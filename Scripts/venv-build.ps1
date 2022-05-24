cd $PSScriptRoot/..

python -m venv .

. ./Scripts/Activate.ps1

pyinstaller --onefile --icon=img/icon/icon.ico main.pyw

if (Test-Path -Path dist/LOST_TOOL.exe) { rm dist/LOST_TOOL.exe }

mv dist/main.exe dist/LOST_TOOL.exe
