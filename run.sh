#!/bin/bash

SRCDIR=${HOME}/code
CONTAINER=simulator

docker run --name=${CONTAINER} -v ${HOME}/code/NEDO/util/polybench-c-3.2:${SRCDIR} \
       riken/simulator \
       aarch64-linux-gnu-gcc-8 -static -O3 \
       -I${SRCDIR}/utilities/ -I${SRCDIR}/stencils/jacobi-1d-imper/ \
       ${SRCDIR}/utilities/polybench.c ${SRCDIR}/stencils/jacobi-1d-imper/jacobi-1d-imper.c \
       -DLARGE_DATASET \
       -o jacobi-1d-imper
