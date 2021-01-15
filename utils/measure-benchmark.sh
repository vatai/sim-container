
BENCHMARK=${BENCHMARK:-stencils/jacobi-1d}
SRCDIR=${SRCDIR:-"./polybench-c-4.2.1-beta"}
NAME="$(basename ${BENCHMARK})"
DATASET=MEDIUM_DATASET
BIN=${NAME}-${DATASET}
BINDIR=bin

mkdir -p ${BINDIR}
${CC} -I${SRCDIR}/utilities/ -I${SRCDIR}/${BENCHMARK}/ \
       ${SRCDIR}/utilities/polybench.c ${SRCDIR}/${BENCHMARK}/${NAME}.c \
       -D${DATASET} -DPOLYBENCH_TIME -lm \
       -o ${BINDIR}/${BIN}

python utils/measure.py ${BINDIR}/${BIN}
