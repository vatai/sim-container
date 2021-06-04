#!/bin/bash

list=$1

cat $list | while read line; do
    bin=$(echo $line | cut -d\  -f1)
    core=$(echo $line | cut -d\  -f2)
    screen -d -m bash -c ../sim-container/run-dynamic.sh $bin $core
done
