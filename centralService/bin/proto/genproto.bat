protoc.exe -I../../src/AdminServer/adminProto/webservice --go_out=plugins=grpc:../../src/AdminServer/adminProto/webservice adminWebService.proto

protoc.exe -I../../src/AdminServer/adminProto/gsmanager --go_out=../../src/AdminServer/adminProto/gsmanager adminServer.proto
protoc.exe -I../../src/centralLogin/centralLoginApp/clientService --go_out=../../src/centralLogin/centralLoginApp/clientService centralLogin.proto
protoc.exe -I../../src/centralLogin/centralLoginApp/gameServerService --go_out=../../src/centralLogin/centralLoginApp/gameServerService gameServerLogin.proto
protoc.exe -I../../src/router/routerApp/gameServerService --go_out=../../src/router/routerApp/gameServerService gameServerRouter.proto
protoc.exe -I../../src/queueServer/queueApp/clientService --go_out=../../src/queueServer/queueApp/clientService clientServerQueue.proto
protoc.exe -I../../src/queueServer/queueApp/gameServerService --go_out=../../src/queueServer/queueApp/gameServerService gameServerQueue.proto


protoc.exe -I../../src/auction/auctionApp/gameServerService --go_out=../../src/auction/auctionApp/gameServerService gameServerAuction.proto
protoc.exe -I../../src/dropServer/dropApp/gameServerService --go_out=../../src/dropServer/dropApp/gameServerService gameServerDrop.proto
protoc.exe -I../../src/crossDataServer/crossDataApp/gameServerService --go_out=../../src/crossDataServer/crossDataApp/gameServerService gameServerCrossData.proto

protoc.exe -I../../src/AdminServer/adminProto/gsmanager --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/AdminServer/adminProto/gsmanager adminServer.proto
protoc.exe -I../../src/centralLogin/centralLoginApp/clientService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/centralLogin/centralLoginApp/clientService centralLogin.proto
protoc.exe -I../../src/centralLogin/centralLoginApp/gameServerService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/centralLogin/centralLoginApp/gameServerService gameServerLogin.proto
protoc.exe -I../../src/router/routerApp/gameServerService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/router/routerApp/gameServerService gameServerRouter.proto
protoc.exe -I../../src/queueServer/queueApp/clientService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/queueServer/queueApp/clientService clientServerQueue.proto
protoc.exe -I../../src/queueServer/queueApp/gameServerService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/queueServer/queueApp/gameServerService gameServerQueue.proto


protoc.exe -I../../src/auction/auctionApp/gameServerService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/auction/auctionApp/gameServerService gameServerAuction.proto

protoc.exe -I../../src/dropServer/dropApp/gameServerService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/dropServer/dropApp/gameServerService gameServerDrop.proto
protoc.exe -I../../src/crossDataServer/crossDataApp/gameServerService --plugin=protoc-gen-custom=rpc_plugin.bat --custom_out=../../src/crossDataServer/crossDataApp/gameServerService gameServerCrossData.proto

@rem python start
set curpath=%~dp0
set srcPath=%curpath%/../../src
cd protoc-3.6.1-win32/bin
protoc.exe -I%srcPath%/dropServer/dropApp/gameServerService --python_out=%srcPath%/dropServer/dropApp/gameServerService gameServerDrop.proto
protoc.exe -I%srcPath%/centralLogin/centralLoginApp/gameServerService --python_out=%srcPath%/centralLogin/centralLoginApp/gameServerService gameServerLogin.proto
protoc.exe -I%srcPath%/crossDataServer/crossDataApp/gameServerService --python_out=%srcPath%/crossDataServer/crossDataApp/gameServerService gameServerCrossData.proto
@pause
