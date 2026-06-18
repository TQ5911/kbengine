@echo off

python --version || python3 --version > nul 2>&1

if %errorlevel% equ 0 (
    @color 0A
    echo python is installed
) else (
    @color 04
    echo Please install python firstly !
    echo Download URL: https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe
    echo Tips: When you install python, please tick "Add python.exe to PATH" option.
    pause
)

echo on

set curpath=%~dp0

cd ..
set KBE_ROOT=%cd%
set KBE_RES_PATH=%KBE_ROOT%/kbe/res/;%curpath%/;%curpath%/scripts/;%curpath%/res/
set KBE_BIN_PATH=%KBE_ROOT%/kbe/bin/server/

if defined uid (echo UID = %uid%) else set uid=%random%%%32760+1

echo KBE_ROOT = %KBE_ROOT%
echo KBE_RES_PATH = %KBE_RES_PATH%
echo KBE_BIN_PATH = %KBE_BIN_PATH%

cd %curpath%

%KBE_BIN_PATH%/kbcmd.exe --clientsdk=unity --outpath=scripts\kbengine_unity3d_plugins
%KBE_BIN_PATH%/kbcmd.exe --clientsdk=bot --outpath=scripts\bots

cd %curpath%/scripts/kbengine_unity3d_plugins
python ModifyProperty.py


cd %curpath%
.\tools\gen_lua\gen_client_lua.exe --config .\tools\gen_lua\config.json
move /y ".\scripts\bots\*py" "..\..\..\..\tools\gamebot\scripts\bots"

@pause
