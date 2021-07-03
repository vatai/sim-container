#!/bin/bash

list=$1

cat $list | sed -e '/^#/d' | while read line; do
    core=$(echo $line | cut -d\;  -f1)
    num_threads=$(echo $line | cut -d\; -f2)
    bin=$(echo $line | cut -d\; -f3)
    args="$(echo $line | cut -d\; -f4)"
    screen -S C${core}.$(basename $bin) -d -m bash -c "../sim-container/run-dynamic.sh $core $num_threads $bin '$args'"
done
