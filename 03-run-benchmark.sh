#!/bin/bash

source env.source

docker run --rm \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/configs/example/se.py \
       --cpu-type=O3_ARM_PostK_3 --caches \
       --l2cache --l2_size=${CACHE_SIZE} \
       -c ${BINDIR}/${BIN}
