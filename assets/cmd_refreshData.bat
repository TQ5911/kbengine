@echo off
set curpath=%~dp0

for /f "tokens=1,2 delims==" %%i in (uidcfg.cfg) do (
    if "%%i"=="uid" set uid=%%j)

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/


cd %curpath%


echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

python hotReload/_genRefreshData.py
start %KBE_BIN_PATH%/runscript.exe -cell --script=._refreshData.py
start %KBE_BIN_PATH%/runscript.exe -base --script=._refreshData.py


