FROM ubuntu:18.04
MAINTAINER vatai

ARG USER
ARG GROUP
ARG USER_ID
ARG GROUP_ID

ENV HOME /home/${USER}
ENV SHELL /bin/bash

RUN groupadd -g ${GROUP_ID} ${GROUP}
RUN useradd -l -m -u ${USER_ID} -g ${GROUP} ${USER}
RUN gpasswd -a ${USER} sudo
RUN echo "${USER}:userpass" | chpasswd

RUN apt-get update && apt-get install -y \
    g++ \
    g++-8-aarch64-linux-gnu \
    libgoogle-perftools-dev \
    protobuf-compiler \
    libprotobuf-dev \
    git \
    m4 \
    python-dev \
    make \
    scons \
    sudo \
    vim \
    zlib1g-dev

RUN apt-get clean

RUN chmod o+w /etc/sudoers
RUN sed -i -e 's/%sudo\tALL=(ALL:ALL) ALL/%sudo\tALL=(ALL) NOPASSWD: ALL/'  /etc/sudoers
RUN chmod o-w /etc/sudoers

WORKDIR /opt
RUN git clone https://github.com/RIKEN-RCCS/riken_simulator.git
WORKDIR riken_simulator
RUN sed -i "369,372s:^:#:" SConstruct
RUN scons build/ARM/gem5.opt -j $(nproc)

# RUN sed -i -e 's/\(--cpu-type=O3_ARM_PostK_3\)/& --caches --l1d_size=128kB --l1i_size=128kB --l2cache --l2_size=42MB --mem_bus_width=128 --mem_resp_width=256/' util/run-pa

USER ${USER}:${GROUP}
WORKDIR ${HOME}
echo "export PATH=/opt/riken_simulator/util:/opt/riken_simulator/bin"