FROM riken/simulator

ARG USER
ARG GROUP
ARG USER_ID
ARG GROUP_ID

ENV HOME /home/${USER}
ENV SHELL /bin/bash

# RUN groupadd -g ${GROUP_ID} ${GROUP}
# RUN useradd -l -m -u ${USER_ID} -g ${GROUP} ${USER}
# RUN gpasswd -a ${USER} sudo
# RUN echo "${USER}:userpass" | chpasswd

WORKDIR ${HOME}/riken_simulator

# Fix SnoopMask
RUN sed -i '69,71 {s!^!// !}' src/mem/cache/tags/base_set_assoc.cc
RUN sed -i '117,119 {s!^!// !}' src/mem/snoop_filter.hh
RUN sed -i 's/typedef uint64_t SnoopMask;/typedef unsigned long long SnoopMask;/' src/mem/snoop_filter.hh

# Build gem5
RUN scons build/ARM/gem5.opt -j $(nproc)

# RUN sudo sed -i -e 's/\(--cpu-type=O3_ARM_PostK_3\)/& --caches --l1d_size=128kB --l1i_size=128kB --l2cache --l2_size=32MB --mem_bus_width=128 --mem_resp_width=256/' util/run-pa

USER ${USER}:${GROUP}
WORKDIR ${HOME}
RUN echo "export PATH=${HOME}/riken_simulator/util:${PATH}" >> ${HOME}/.bashrc