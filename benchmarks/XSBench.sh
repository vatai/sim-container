sed -i -e 's/CC = gcc/CC = aarch64-linux-gnu-gcc-8 -static -O3/' ${SRCDIR}/XSBench/src/Makefile
make -C ${SRCDIR}/XSBench/src/
cp ${SRCDIR}/CSBench/src/${BIN} ${BINDIR}/
