#!/bin/bash

# See env.source to select which benchmark to compile/run.
source env.source

umask 022; mkdir -m755 -p ${HOST_BINDIR}

docker run --rm \
       --env SRCDIR=${SRCDIR} \
       --env BINDIR=${BINDIR} \
       --env BIN=${BIN} \
       -v ${HOST_SRCDIR}:${SRCDIR} \
       -v ${HOST_BINDIR}:${BINDIR} \
       ${DOCKER_IMAGE} \
       ${COMPILE_CMD}
