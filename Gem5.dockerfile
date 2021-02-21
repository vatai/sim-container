FROM ubuntu:20.04
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

RUN apt update && apt install -y \
    g++ \
    g++-aarch64-linux-gnu \
    libgoogle-perftools-dev \
    libprotobuf-dev \
    libpng-dev \
    protobuf-compiler \
    git \
    m4 \
    python3-dev \
    python3-six \
    make \
    scons \
    sudo \
    vim \
    python-is-python3 \
    zlib1g-dev
#    cmake

RUN apt clean

RUN chmod o+w /etc/sudoers
RUN sed -i -e 's/%sudo\tALL=(ALL:ALL) ALL/%sudo\tALL=(ALL) NOPASSWD: ALL/'  /etc/sudoers
RUN chmod o-w /etc/sudoers

USER ${USER}:${GROUP}
WORKDIR ${HOME}

RUN git clone https://gem5.googlesource.com/public/gem5
WORKDIR gem5
RUN scons build/ARM/gem5.opt -j $(nproc)

WORKDIR ${HOME}
