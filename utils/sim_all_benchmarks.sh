#!/bin/bash

for BENCHMARK in $(./utils/iterate_benchmarks.sh); do
    POLYBENCH=${BENCHMARK} ./02-compile-benchmark.sh
    POLYBENCH=${BENCHMARK} ./03-run-benchmark.sh
done
