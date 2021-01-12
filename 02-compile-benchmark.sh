#!/bin/bash

# See env.source to select which benchmark to compile/run.
source env.source

mkdir -m744 -p ${HOST_BINDIR}
docker run --rm \
       -v ${HOST_SRCDIR}:${SRCDIR} \
       -v ${HOST_BINDIR}:${BINDIR} \
       riken/simulator \
       ${COMPILE_CMD}
