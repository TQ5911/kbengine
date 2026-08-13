#!/bin/bash
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

svn propset svn:executable on ./login/centralLogin
svn propset svn:executable on ./login/game.sh

svn propset svn:executable on ./orderService/orderService
svn propset svn:executable on ./orderService/game.sh

svn propset svn:executable on ./allianceService/allianceService
svn propset svn:executable on ./allianceService/game.sh

svn propset svn:executable on ./leaseServer/leaseServer
svn propset svn:executable on ./leaseServer/game.sh

svn propset svn:executable on build_all_server.sh

echo 'Executable permissions on all above are set successfully'


