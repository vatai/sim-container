#!/bin/bash

CC=${CC:-"fcc -Nclang -O3"}

echo "["
for BENCHMARK in $(./utils/iterate_benchmarks.sh); do
    CC=${CC} BENCHMARK=${BENCHMARK} ./utils/measure-benchmark.sh
done
echo "]"

