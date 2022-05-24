cd $PSScriptRoot/..

python -m venv .

. ./Scripts/Activate.ps1

if (Test-Path -Path dist) { rm -r dist }

pyinstaller --name=LOST_TOOL --icon=img/icon/icon.ico main.pyw
