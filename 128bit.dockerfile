FROM riken/simulator

ARG USER
ARG GROUP
ARG USER_ID
ARG GROUP_ID

ENV HOME /home/${USER}
ENV SHELL /bin/bash

WORKDIR ${HOME}/riken_simulator

# Fix SnoopMask
RUN sed -i 's/typedef uint64_t SnoopMask;/typedef unsigned __int128 SnoopMask;/' src/mem/snoop_filter.hh
RUN sed -i '38 i std::ostream& operator<<(std::ostream& d, const unsigned __int128 v);' src/base/cprintf_formats.hh
RUN sed -i '41 i ostream& operator<<(ostream& d, const unsigned __int128 v) { d << "128int Hi:" << (void*)v << ";Lo:" << (void*)(v >> 64); return d;}' src/base/cprintf.cc

# Build gem5
RUN scons build/ARM/gem5.opt -j $(nproc)

# RUN sudo sed -i -e 's/\(--cpu-type=O3_ARM_PostK_3\)/& --caches --l1d_size=128kB --l1i_size=128kB --l2cache --l2_size=32MB --mem_bus_width=128 --mem_resp_width=256/' util/run-pa

USER ${USER}:${GROUP}
WORKDIR ${HOME}
