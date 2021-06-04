#!/bin/bash

BIN=$1

./build/ARM/gem5.opt -d "m5/$(basename $BIN)" ./configs/example/se.py \
	--cpu-type=O3_ARM_PostK_3 \
	--caches --l2cache \
	-e ../sim-container/fj_env.txt -n 1 \
	-c ../sim-container/ld-linux-aarch64.so.1 \
	-o ${BIN} > "m5/$(basename $BIN).output.txt"
