FROM ubuntu:18.04
MAINTAINER vatai

ENV USER user
ENV HOME /home/${USER}
ENV SHELL /bin/bash

RUN useradd -m ${USER}
RUN gpasswd -a ${USER} sudo
RUN echo 'user:userpass' | chpasswd

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

RUN chmod o+w /etc/sudoers \
  && sed -i -e 's/%sudo\tALL=(ALL:ALL) ALL/%sudo\tALL=(ALL) NOPASSWD: ALL/'  /etc/sudoers \
  && chmod o-w /etc/sudoers

USER ${USER}
WORKDIR ${HOME}
RUN git clone --depth 1 https://github.com/RIKEN-RCCS/riken_simulator.git
RUN sed -i -e 's!PREFIX=/opt/riken_simulator!PREFIX=/home/user/riken_simulator!' riken_simulator/util/gem5-o3
RUN echo TADAM > file.txt

WORKDIR ${HOME}/riken_simulator
RUN sed -i "369,372s:^:#:" SConstruct
RUN scons build/ARM/gem5.opt -j $(nproc)

