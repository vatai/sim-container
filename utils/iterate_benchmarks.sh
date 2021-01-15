#!/bin/bash

SRCDIR=${SRCDIR:-"./polybench-c-4.2.1-beta"}

for DIR in $(find ${SRCDIR} -type d); do
    NAME=$(basename ${DIR})
    if [ -f ${DIR}/${NAME}.c ]; then
        echo ${DIR} | sed -e "s!${SRCDIR}/!!"
    fi
done

