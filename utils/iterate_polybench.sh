#!/bin/bash

SRCDIR=${SRCDIR:-"./benchmarks/polybench-c-4.2.1-beta"}
# LIST_FILE=${LIST_FILE:-"polybench_list.txt"}

# if [ -e ${LIST_FILE} ]; then
#     # If ${LIST_FILE} exists iterate uncommented lines.
#     sed -e '/^#/d' ${LIST_FILE}
# else
# Otherwise iterate all benchmarks.
for DIR in $(find ${SRCDIR} -type d); do
    NAME=$(basename ${DIR})
    if [ -f ${DIR}/${NAME}.c ]; then
        echo ${DIR} | sed -e "s!${SRCDIR}/!!"
    fi
done
# fi


