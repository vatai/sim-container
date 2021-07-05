#!/bin/bash

script_name=$0
core=$1
num_threads=$2
BIN=$3
BM=$(basename $BIN)
shift
shift
shift

if [[ -z $GEM5DIR ]]; then
  echo 'Please set $GEM5DIR first'
  exit -1
fi

if [[ "" -ne $core ]]; then
  pin_cmd="numactl -C $core"
fi

l2_bankbit=${l2_bankbit:-2}
l2_bus_width=${l2_bus_width:-64}
l2_resp_width=${l2_resp_width:-128}

suffix=$(echo "$@" | sed 's/ /_/g')
out_path=${BM}${suffix}_numthreads${num_threads}_bankbit${l2_bankbit}_buswidth${l2_bus_width}_respwidth${l2_resp_width}

fjenv=/tmp/${BM}${core}fjenv${num_threads}.txt
echo -e "LD_LIBRARY_PATH=${GEM5DIR}/../lib\nOMP_NUM_THREADS=${num_threads}\nFLIB_USE_CPURESOURCE_LIBOMP=FALSE" > $fjenv

$pin_cmd $GEM5DIR/build/ARM/gem5.opt -d "${GEM5DIR}/m5/${out_path}" $GEM5DIR/configs/example/se.py \
	--cpu-type=O3_ARM_PostK_3 \
	--caches --l2cache \
	--mem-size=32GB \
	--l2_bankbit=${l2_bankbit} \
	--l2_bus_width=${l2_bus_width} \
	--l2_resp_width=${l2_resp_width} \
	-e $fjenv -n $num_threads \
	-c ${GEM5DIR}/../lib/ld-linux-aarch64.so.1 \
	-o "${BIN} $@" \
        1> "${GEM5DIR}/m5/${out_path}.stdout.txt" \
        2> "${GEM5DIR}/m5/${out_path}.stderr.txt"

