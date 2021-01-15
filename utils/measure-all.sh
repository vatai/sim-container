#!/bin/bash

CC=${CC:-"fcc -Nclang -O3"}
SRCDIR=${SRCDIR:-"./polybench-c-4.2.1-beta"}
DIRS=$(find ${SRCDIR} -type d)

echo "["
for BENCHMARK in $(./utils/iterate_benchmarks.sh); do
    CC=${CC} BENCHMARK=${BENCHMARK} ./utils/measure-benchmark.sh
done
echo "]"

