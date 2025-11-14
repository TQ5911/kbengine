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
svn propset svn:executable on ./admin/game_admin.sh

svn propset svn:executable on ./auction/auction
svn propset svn:executable on ./auction/game_auction.sh

svn propset svn:executable on ./crossDataServer/crossDataServer
svn propset svn:executable on ./crossDataServer/game_cross_data_server.sh

svn propset svn:executable on ./dropServer/dropServer
svn propset svn:executable on ./dropServer/game_drop_server.sh

svn propset svn:executable on ./maple/maple
svn propset svn:executable on ./maple/game_maple.sh

svn propset svn:executable on ./router/router
svn propset svn:executable on ./router/game_router.sh

svn propset svn:executable on ./login/centralLogin
svn propset svn:executable on ./login/game_login.sh

svn propset svn:executable on build_all_server.sh

svn propset svn:executable on set_svn_executable_props.sh

echo Executable permissions on all above are set successfully

@pause

