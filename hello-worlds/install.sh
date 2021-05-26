#!/bin/bash

gcc hello.c -o hello.gcc
gcc omp-hello.c -fopenmp -o omp-hello.gcc
fcc hello.c -Knolargepage -o hello.nolargepage.fcc
fcc omp-hello.c -Knolargepage -fopenmp -o omp-hello.nolargepage.fcc
