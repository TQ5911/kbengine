@echo off
set curpath=%~dp0


cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/
set uid=489

if defined uid (echo UID = %uid%) else set uid=%random%%%32760+1

echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

cd %curpath%
echo %curpath%

%KBE_BIN_PATH%/runscript.exe -cell --script=_reload.py
%KBE_BIN_PATH%/runscript.exe -base --script=_reload.py
