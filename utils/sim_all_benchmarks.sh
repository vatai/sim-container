#!/bin/bash

for BENCHMARK in $(./utils/iterate_benchmarks.sh); do
    POLYBENCH=${BENCHMARK} ./03-run-benchmark.sh
done
