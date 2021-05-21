#!/bin/bash
#PJM -L "rscunit=rscunit_ft01,rscgrp=small"
#PJM -L elapse=01:00:00
#PJM -L "node=1"
#PJM -j
#PJM -S
#PJM --llio sharedtmp-size=80Gi


wget https://downloads.sourceforge.net/project/scons/scons/1.3.1/scons-1.3.1.tar.gz
tar xzf scons-1.3.1.tar.gz
cd scons-1.3.1
python2 setup.py install --user
cd -

git clone https://github.com/RIKEN-RCCS/riken_simulator/
cd riken_simulator
sed -i "369,372s:^:#:" ./SConstruct
sed -i -e 's/ exit(/ sys.exit(/g' ./util/cpt_upgrader.py
sed -i -e 's/if NO_FALLOCATE.*/if NO_FALLOCATE==0/' ./src/sim/syscall_emul.cc
python2 $(which scons) build/ARM/gem5.opt -j $(nproc)

