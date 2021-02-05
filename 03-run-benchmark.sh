#!/bin/bash

# See env.source to select which benchmark to compile/run.
source env.source

umask 022; mkdir -m755 -p ${HOST_OUTDIR}

docker run --rm \
       --env BINDIR=${BINDIR} \
       --env OUTDIR=${OUTDIR} \
       --env BIN=${BIN} \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/configs/example/se.py \
       ${SIM_PARAMS} \
       -c ${BINDIR}/${BIN} ${OPTIONS} \
       >> ${HOST_OUTDIR}/output.txt
