@echo off
set curpath=%~dp0

set PROTO_TOOL_PATH=%curpath%/external/proto
set PROTO_SRC_PATH=%curpath%/scripts/common/proto/
set PROTO_OUT_PATH=%curpath%/scripts/common/proto/
set CSHARP_OUT_PATH=%curpath%/../../../../Client/Assets/CSHotUpdate/Scripts/Proto

cd %PROTO_TOOL_PATH%/protoc-3.3.0-csharp/
protoc -I %PROTO_SRC_PATH% --csharp_out=%CSHARP_OUT_PATH% %PROTO_SRC_PATH%/centralLogin.proto

cd %PROTO_TOOL_PATH%/protoc-3.6.1-win32/bin
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% adminServer.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% interface.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% centralLogin.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% gameServerLogin.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% gameServerRouter.proto
protoc -I=%PROTO_SRC_PATH% --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=%CSHARP_OUT_PATH% centralLogin.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% gameServerAuction.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% cross_server.proto
protoc -I=%PROTO_SRC_PATH% --python_out=%PROTO_OUT_PATH% gameServerLease.proto

@pause
