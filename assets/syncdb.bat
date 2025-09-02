@echo off
set curpath=%~dp0

for /f "tokens=1,2 delims==" %%i in (uidcfg.cfg) do (
    if "%%i"=="uid" set uid=%%j)

if defined uid (goto realexc) else (goto setuid)

:realexc
cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/


echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

start %KBE_BIN_PATH%/dbmgr.exe -syncdb --cid=2614000

exit

:setuid
echo "edit uidcfg.cfg to set uid"
pause

exit