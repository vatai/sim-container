#!/usr/bin/bash

FILENAME="omp$1.txt"
echo OMP_NUM_THREADS=$1 > ${FILENAME}
echo OMP_NUM_PARALELL=$1 >> ${FILENAME}
echo FLIB_FASTOMP=FALSE >> ${FILENAME}
echo FLIB_CNTL_BARRIER_ERR=FALSE >> ${FILENAME}

echo -n "$1 -e ${FILENAME}"