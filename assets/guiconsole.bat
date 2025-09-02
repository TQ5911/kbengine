@echo off
set curpath=%~dp0


for /f "tokens=1,2 delims==" %%i in (uidcfg.cfg) do (
    if "%%i"=="uid" set uid=%%j)


cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/


cd %KBE_ROOT%/kbe/tools/server/guiconsole/
start guiconsole.exe
