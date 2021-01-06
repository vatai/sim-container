FROM ubuntu:18.04
MAINTAINER vatai

ARG USER
ARG USER_ID
ARG GROUP_ID

ENV HOME /home/${USER}
ENV SHELL /bin/bash

RUN groupadd -g ${GROUP_ID} ${USER}
RUN useradd -l -m -u ${USER_ID} -g ${USER} ${USER}
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

RUN pwd && whoami
USER ${USER}
WORKDIR ${HOME}
USER pwd && whoami
RUN git clone --depth 1 https://github.com/RIKEN-RCCS/riken_simulator.git
RUN sed -i -e 's!PREFIX=/opt/riken_simulator!PREFIX=/home/user/riken_simulator!' riken_simulator/util/gem5-o3

WORKDIR ${HOME}/riken_simulator
RUN sed -i "369,372s:^:#:" SConstruct
RUN scons build/ARM/gem5.opt -j $(nproc)

WORKDIR ${HOME}