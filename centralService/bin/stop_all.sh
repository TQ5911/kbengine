#!/bin/bash

cd login
./game_login.sh stop

cd ../admin
./game_admin.sh stop

cd ../router
./game_router.sh stop

cd ../maple
./game_maple.sh stop

cd ../dropServer
./game_drop_server.sh stop

cd ../auction
./game_auction.sh stop

cd ../crossDataServer
./game_cross_data_server.sh stop

cd ../queueServer
./game_queue_server.sh stop


ps -ef |grep -v grep | grep -E 'centralLogin|admin|auction|router|maple|dropServer|crossDataServer'