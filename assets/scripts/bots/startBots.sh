#!/bin/bash
if [ $# != 2 ]
then
    echo "usage: start.sh botAuc bot_name"
    exit
fi
numPerProcess=2
numPerSec=1
nProcess=1

toIdx=`expr $nProcess - 1`
for i in $(seq 0 $toIdx); do
    idx=$[$i*$numPerProcess]
    echo "start bot from idx $idx"
    python3 runBots.py $1 $2 $numPerProcess $numPerSec $idx&
done
