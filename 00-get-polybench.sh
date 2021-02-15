#!/bin/bash

POLYBENCH_DIR=polybench-c-4.2.1-beta
POLYBENCH_ARCHIVE=${POLYBENCH_DIR}.tar.gz
URL_PREFIX=https://downloads.sourceforge.net/project/polybench/

cd benchmarks

if [ ! -f ${POLYBENCH_ARCHIVE} ]; then
    # wget http://web.cse.ohio-state.edu/\~pouchet.2/software/polybench/download/polybench-c-3.2.tar.gz
    wget ${URL_PREFIX}${POLYBENCH_ARCHIVE}
fi
if [ ! -d ${POLYBENCH_DIR} ]; then
	# tar xzf polybench-c-3.2.tar.gz
	tar xzf ${POLYBENCH_ARCHIVE}
fi
