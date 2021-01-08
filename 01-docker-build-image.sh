#!/bin/bash

docker build \
    --build-arg USER=$(id -un) \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP=$(id -gn) \
    --build-arg GROUP_ID=$(id -g) \
    -t riken/simulator .
