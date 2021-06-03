CC=${CC:-gcc}
CFLAGS=${CFLAGS:-"-O3"}
DS=${DS:-MEDIUM_DATASET}
BMDIR=${BMDIR:-./linear-algebra/solvers/gramschmidt}
BM=${BM:-$(basename $BMDIR)}

$CC $CFLAGS \
	-I ./utilities/ -I ./$BMDIR/$BM ./utilities/polybench.c \
	$BMDIR/$BM.c -D$DS -DPOLYBENCH_TIME -lm \
	-o $BM.$DS.$CC
