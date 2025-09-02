#!/bin/sh
./game_baseapp.sh stop 1 &
./game_baseapp.sh stop 2 &

./game_cellapp.sh stop 1 &
./game_cellapp.sh stop 2 &

./game_interfaces.sh stop 1 7

./game_dbmgr.sh stop 1 &

./game_baseappmgr.sh stop 1 &

./game_cellappmgr.sh stop 1 &

./game_loginapp.sh stop 1 &

./game_machine.sh stop 1 &

./game_logger.sh stop 1 &

