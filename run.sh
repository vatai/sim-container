#!/bin/bash

SRCDIR=${HOME}/code
OUTDIR=${HOME}/m5out
HOST_OUTDIR=$(pwd)/tmp
CONTAINER=simulator

mkdir ${HOST_OUTDIR}
chmod o+rX ${HOST_OUTDIR}

docker run --rm --name=${CONTAINER} \
       -v ${HOME}/code/NEDO/util/polybench-c-3.2:${SRCDIR} \
       -v ${HOST_OUTDIR}:${OUTDIR} \
       riken/simulator \
       aarch64-linux-gnu-gcc-8 -static -O3 \
       -I${SRCDIR}/utilities/ -I${SRCDIR}/stencils/jacobi-1d-imper/ \
       ${SRCDIR}/utilities/polybench.c ${SRCDIR}/stencils/jacobi-1d-imper/jacobi-1d-imper.c \
       -DLARGE_DATASET \
       -o ${OUTDIR}/jacobi-1d-imper
