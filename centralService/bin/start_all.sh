#!/bin/bash

cd login
./game_login.sh stop
./game_login.sh start

cd ../admin
./game_admin.sh stop
./game_admin.sh start

cd ../router
./game_router.sh stop
./game_router.sh start

cd ../maple
./game_maple.sh stop
./game_maple.sh start

cd ../dropServer
./game_drop_server.sh stop
./game_drop_server.sh start

cd ../auction
./game_auction.sh stop
./game_auction.sh start

cd ../crossDataServer
./game_cross_data_server.sh stop
./game_cross_data_server.sh start

cd ../queueServer
./game_queue_server.sh stop
./game_queue_server.sh start

ps -ef |grep -v grep | grep -E 'centralLogin|admin|auction|router|maple|dropServer|crossDataServer'
