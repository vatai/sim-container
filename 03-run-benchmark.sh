#!/bin/bash

# See env.source to select which benchmark to compile/run.
source env.source

umask 022; mkdir -m755 -p ${HOST_OUTDIR}

HOST_ENV_FILE=${HOST_BINDIR}/${ENV_FILE}
echo "OMP_NUM_THREADS=${NCORES}" > "$HOST_ENV_FILE"
echo "OMP_NUM_PARALELL=${NCORES}" >> "$HOST_ENV_FILE"
echo "FLIB_FASTOMP=FALSE" >> "$HOST_ENV_FILE"
echo "FLIB_CNTL_BARRIER_ERR=FALSE" >> "$HOST_ENV_FILE"


docker run --rm \
       --env BINDIR=${BINDIR} \
       --env OUTDIR=${OUTDIR} \
       --env BIN=${BIN} \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       ${DOCKER_IMAGE} \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/${GEM5_CONFIG} \
       ${SIM_PARAMS} \
       -c ${BINDIR}/${BIN} -o "${RUN_OPTIONS}" \
       1>> ${HOST_OUTDIR}/output-and-error.txt \
       2>&1
