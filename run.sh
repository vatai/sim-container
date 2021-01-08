#!/bin/bash

SIMDIR=${HOME}/riken_simulator
BIN=jacobi-1d-imper
SRCDIR=/tmp/src
BINDIR=/tmp/bin
OUTDIR=${HOME}/m5out

HOST_SRCDIR=${HOME}/code/NEDO/util/polybench-c-3.2

HOST_BINDIR=$(pwd)/bin
HOST_OUTDIR=$(pwd)/tmp
mkdir -p ${HOST_BINDIR}
chmod o+rX ${HOST_BINDIR}
mkdir -p ${HOST_OUTDIR}
chmod o+rX ${HOST_OUTDIR}

docker run --rm \
       -v ${HOST_SRCDIR}:${SRCDIR} \
       -v ${HOST_BINDIR}:${OUTDIR} \
       riken/simulator \
       aarch64-linux-gnu-gcc-8 -static -O3 \
       -I${SRCDIR}/utilities/ -I${SRCDIR}/stencils/jacobi-1d-imper/ \
       ${SRCDIR}/utilities/polybench.c ${SRCDIR}/stencils/jacobi-1d-imper/jacobi-1d-imper.c \
       -DMINI_DATASET \
       -o ${OUTDIR}/${BIN}

# create exe in ${HOST_OUTDIR}

docker run --rm \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/configs/example/se.py \
       --cpu-type=O3_ARM_PostK_3 --caches \
       --l2cache --l2_size=1024MB \
       -c ${BINDIR}/${BIN}
