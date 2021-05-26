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
sed -i -e "s#PREFIX=/opt/riken_simulator#PREFIX=$ROOTDIR/dep/$BM#g" ./util/gem5-o3
sed -i "369,372s:^:#:" ./SConstruct
sed -i -e 's/ exit(/ sys.exit(/g' ./util/cpt_upgrader.py
sed -i -e 's/if NO_FALLOCATE.*/if NO_FALLOCATE==0/' ./src/sim/syscall_emul.cc
sed -i -e 's/const Addr PageShift = 25;/const Addr PageShift = 16;/' ./src/arch/arm/isa_traits.hh
sed -i 's/typedef uint64_t SnoopMask;/typedef unsigned __int128 SnoopMask;/' ./src/mem/snoop_filter.hh
sed -i '38 i std::ostream& operator<<(std::ostream& d, const unsigned __int128 v);' ./src/base/cprintf_formats.hh
sed -i '41 i ostream& operator<<(ostream& d, const unsigned __int128 v) { d << "128int Hi:" << (void*)v << ";Lo:" << (void*)(v >> 64); return d;}' ./src/base/cprintf.cc
python2 $(which scons) build/ARM/gem5.opt -j $(nproc)

