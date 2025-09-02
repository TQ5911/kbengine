@echo off
set curpath=%~dp0

for /f "tokens=1,2 delims==" %%i in (uidcfg.cfg) do (
    if "%%i"=="uid" set uid=%%j)

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/


echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

cd %curpath%

%KBE_BIN_PATH%/runscript.exe -cell --script=_refresh.py
%KBE_BIN_PATH%/runscript.exe -base --script=_refresh.py