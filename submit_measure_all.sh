#!/bin/bash
source ${HOME}/bin/activate.sh

./utils/measure-all.sh > all_times.json
