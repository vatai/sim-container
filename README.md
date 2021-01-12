## Riken simulator with `docker`
Most of the scripts are self documented and simple enough.

### Building the docker image
`01-docker-build-image.sh` builds a docker image (which can be
verified with the `docker images` command).  Unless this image is
deleted (using the `docker rmi riken/simulator:latest`), this script
does not need to be invoked afterwards.

### Compiling a benchmark
The `02-compile-benchmark.sh` builds a benchmark. See
`jacobi1d.source` about modifying compilation parameters.  See
`env.source` how to switch between benchmarks using `COMPILE_PARAMS`.

### Running a benchmark
The `03-run-benchmark` runs the simulator.  See `sim.source` (and of
course the simulator itself) for details on how to specify different
simulator parameters.

CAUTION: Don't forget to set `COMPILE_PARAMS` if you want to use a
different benchmark.

## Known bugs
If you get some permission error mentioning `mkdir` then loosen your
permissions around of the host source dir.

You need to get your own polybench and set `HOST_SRCDIR` in
`jacobi1d.source`.
