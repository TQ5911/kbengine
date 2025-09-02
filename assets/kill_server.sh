#!/bin/sh
pkill -9 machine
pkill -9 dbmgr
pkill -9 cellappmgr
pkill -9 baseappmgr
pkill -9 cellapp
pkill -9 baseapp
pkill -9 loginapp
pkill -9 bots
pkill -9 logger
pkill -9 interfaces

PROCESS=`ps -ef|grep logFilter|grep -v grep|grep -v PPID|awk '{ print $2}'`
for i in $PROCESS
do
  echo "Kill the logFilter process [ $i ]"
  kill -9 $i
done