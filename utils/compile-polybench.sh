CC=${CC:-gcc}
DS=${DS:-MEDIUM_DATASET}
BMDIR=${BMDIR:-./linear-algebra/solvers/gramschmidt}
BM=${BM:-gramschmidt}

$CC -O3 \
	-I ./utilities/ -I ./$BMDIR/$BM ./utilities/polybench.c \
	$BMDIR/$BM.c -D$DS -DPOLYBENCH_TIME -lm \
	-o $BM.$DS.$CC
