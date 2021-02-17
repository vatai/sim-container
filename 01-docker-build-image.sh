#!/bin/bash

# You don't need to change anything here.  If you do tell me.  You
# might want to change something in the Dockerfile -- Emil

docker build \
    --build-arg USER=$(id -un) \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP=$(id -gn) \
    --build-arg GROUP_ID=$(id -g) \
    -t riken/simulator .

docker build \
    --build-arg USER=$(id -un) \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP=$(id -gn) \
    --build-arg GROUP_ID=$(id -g) \
    -f Gem5.dockerfile \
    -t riken/gem5 .
