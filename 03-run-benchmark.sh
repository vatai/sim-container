#!/bin/bash

source env.source

mkdir -p ${HOST_OUTDIR}
chmod o+rX ${HOST_OUTDIR}

docker run --rm \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/configs/example/se.py \
       ${SIM_PARAMS} -c ${BINDIR}/${BIN}
