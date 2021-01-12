#!/bin/bash

# See env.source to select which benchmark to compile/run.
source env.source

mkdir -p -m744 ${HOST_OUTDIR}

docker run --rm \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/configs/example/se.py \
       ${SIM_PARAMS} -c ${BINDIR}/${BIN}
