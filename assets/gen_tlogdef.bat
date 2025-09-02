@echo off
set curpath=%~dp0

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/


echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%
cd %curpath%

%KBE_ROOT%/../../../tools/tlogdef-gen/bin/tlogdef_gen.exe external\tencent\JingFenTlog_V1.3.3.xml scripts\server_common\gametlog.py

PAUSE