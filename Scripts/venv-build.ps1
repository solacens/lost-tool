cd $PSScriptRoot/..

python -m venv .

. ./Scripts/Activate.ps1

if (Test-Path -Path dist) { rm -r dist }

pyinstaller "LOST TOOL.spec"
