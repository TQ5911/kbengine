@echo off
svn --version > nul 2>&1

if %errorlevel% equ 0 (
    @color 0A
    echo svn is installed
) else (
    @color 04
    echo Please install svn command-line tools firstly !
    echo Download URL: https://sourceforge.net/projects/tortoisesvn/files/1.14.9/Application/TortoiseSVN-1.14.9.29743-x64-svn-1.14.5.msi/
    echo Tips: When you install TortoiseSVN, please tick "command line client tools" option.
    pause
)

svn propset svn:executable on ./admin/admin
svn propset svn:executable on ./admin/game.sh

svn propset svn:executable on ./auction/auction
svn propset svn:executable on ./auction/game.sh

svn propset svn:executable on ./crossDataServer/crossDataServer
svn propset svn:executable on ./crossDataServer/game.sh

svn propset svn:executable on ./dropServer/dropServer
svn propset svn:executable on ./dropServer/game.sh

svn propset svn:executable on ./maple/maple
svn propset svn:executable on ./maple/game.sh

svn propset svn:executable on ./router/router
svn propset svn:executable on ./router/game.sh

svn propset svn:executable on ./centralLogin/centralLogin
svn propset svn:executable on ./centralLogin/game.sh

svn propset svn:executable on ./orderService/orderService
svn propset svn:executable on ./orderService/game.sh

svn propset svn:executable on ./allianceService/allianceService
svn propset svn:executable on ./allianceService/game.sh

svn propset svn:executable on ./leaseServer/leaseServer
svn propset svn:executable on ./leaseServer/game.sh

svn propset svn:executable on ./queueServer/queueServer
svn propset svn:executable on ./queueServer/game.sh

svn propset svn:executable on build_all_server.sh

svn propset svn:executable on set_svn_executable_props.sh

echo Executable permissions on all above are set successfully

@pause

