#!/bin/bash
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

svn propset svn:executable on ./orderService/orderService
svn propset svn:executable on ./orderService/game_orderService.sh

svn propset svn:executable on build_all_server.sh

echo 'Executable permissions on all above are set successfully'


