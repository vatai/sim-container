#!/bin/bash

if [ ! -f ./polybench-c-3.2.tar.gz ]; then
	wget http://web.cse.ohio-state.edu/\~pouchet.2/software/polybench/download/polybench-c-3.2.tar.gz
fi
if [ ! -d ./polybench-c-3.2 ]; then
	tar xzf polybench-c-3.2.tar.gz
fi
