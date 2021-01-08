#!/bin/bash

SIMDIR=${HOME}/riken_simulator
OUTDIR=${HOME}/m5out
SRCDIR=/tmp/src
BINDIR=/tmp/bin
CC="aarch64-linux-gnu-gcc-8 -static -O3"
CXX="aarch64-linux-gnu-g++-8 -static -O3"

HOST_SRCDIR=${HOME}/code/NEDO/util/polybench-c-3.2
BIN=jacobi-1d-imper
COMPILE_CMD="${CC} -I${SRCDIR}/utilities/ -I${SRCDIR}/stencils/jacobi-1d-imper/ \
       ${SRCDIR}/utilities/polybench.c ${SRCDIR}/stencils/jacobi-1d-imper/jacobi-1d-imper.c \
       -DMINI_DATASET \
       -o ${BINDIR}/${BIN}"

HOST_BINDIR=$(pwd)/bin
mkdir -p ${HOST_BINDIR}
chmod o+rX ${HOST_BINDIR}

docker run --rm \
       -v ${HOST_SRCDIR}:${SRCDIR} \
       -v ${HOST_BINDIR}:${BINDIR} \
       riken/simulator \
       ${COMPILE_CMD}

CACHE_SIZE="1024MB"
HOST_OUTDIR=$(pwd)/${CACHE_SIZE}l2size
mkdir -p ${HOST_OUTDIR}
chmod o+rX ${HOST_OUTDIR}

docker run --rm \
       -v ${HOST_BINDIR}:${BINDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       ${SIMDIR}/build/ARM/gem5.opt \
       ${SIMDIR}/configs/example/se.py \
       --cpu-type=O3_ARM_PostK_3 --caches \
       --l2cache --l2_size=${CACHE_SIZE} \
       -c ${BINDIR}/${BIN}
