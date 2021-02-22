## Riken simulator experiments
Most of the scripts are self documented and simple enough.  There is a
`runner.py` python script, useful to launch multiple jobs based on
yaml config files.

## Overview
- `01-docker-build-image.sh` builds two docker images
- with `02-compile-benchmark.sh` you can compile a benchmark and
- with `03-run-benchmark.sh` you can run a benchmark.

The scripts use environment variables as parameters.  Most of the
environment variables are in the [env.source](env.source) file, which
in turn sources a benchmark specific file.

## The runner scripts
Instead of `02-compile-benchmark.sh` and `03-run-benchmark.sh` the `runner.py` script can be use:
```
python -m runner <path to yaml file>`
```
see examples in [benchmarks](benchmarks) directory.

## Known bugs
If you get some permission error mentioning `mkdir` then loosen your
permissions (probably `chmod o+rx` on the parent directory it
complains about).

## Running the container
Check out what are the variables in `env.source`.
```
docker run --rm -it \
       -v ${HOST_SRCDIR}:/tmp/src \
       -v ${HOST_BINDIR}:/tmp/bin \
       riken/simulator \
       /bin/bash
```
