#!/bin/bash

source env.source

mkdir -p ${HOST_BINDIR}
chmod o+rX ${HOST_BINDIR}
docker run --rm \
       -v ${HOST_SRCDIR}:${SRCDIR} \
       -v ${HOST_BINDIR}:${BINDIR} \
       riken/simulator \
       ${COMPILE_CMD}
