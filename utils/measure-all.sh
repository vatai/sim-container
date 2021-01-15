SRCDIR=${SRCDIR:-"./polybench-c-4.2.1-beta"}
DIRS=$(find ${SRCDIR} -type d)

for DIR in ${DIRS}; do
    NAME=$(basename ${DIR})
    if [ -f ${DIR}/${NAME}.c ]; then
        BENCHMARK=$(echo ${DIR} | sed -e "s!${SRCDIR}/!!")
        BENCHMARK=${BENCHMARK} ./utils/measure-benchmark.sh
    fi
done

