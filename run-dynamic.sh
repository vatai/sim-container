#!/bin/bash

core=$1
num_threads=$2
BIN=$3
BM=$(basename $BIN)
shift
shift
shift

echo "xxx ${BIN} $@ xxx"

if [[ -z $GEM5DIR ]]; then
  echo 'Please set $GEM5DIR first'
  exit -1
fi

if [[ "" -ne $core ]]; then
  pin_cmd="numactl -C $core"
fi

suffix=$(echo $@ | sed 's/ /_/g')
out_path=${BM}${suffix}_numthreads$num_threads


fjenv=/tmp/fjenv${num_threads}.txt
sed s/THREADS=.*/THREADS=${num_threads}/ ../sim-container/fj_env.txt > $fjenv

$pin_cmd $GEM5DIR/build/ARM/gem5.opt -d "m5/${out_path}" $GEM5DIR/configs/example/se.py \
	--cpu-type=O3_ARM_PostK_3 \
	--caches --l2cache \
	--mem-size=32GB \
	-e $fjenv -n $num_threads \
	-c ../sim-container/ld-linux-aarch64.so.1 \
	-o "${BIN} $@" \
        1> "m5/${out_path}.stdout.txt" \
        2> "m5/${out_path}.stderr.txt"
