#!/bin/bash

BIN=$1
BM=$(basename $1)
core=$2

if [[ "" -ne $core ]]; then
  pin_cmd="numactl -C $core"
fi

$pin_cmd ./build/ARM/gem5.opt -d "m5/$BM" ./configs/example/se.py \
	--cpu-type=O3_ARM_PostK_3 \
	--caches --l2cache \
	-e ../sim-container/fj_env.txt -n 1 \
	-c ../sim-container/ld-linux-aarch64.so.1 \
	-o ${BIN} \
        1> "m5/${BM}.stdout.txt" \
        2> "m5/${BM}.stderr.txt"
