1. Compile `riken_simulator` with the `fugaku-install.sh` script.
2. Obtain `ld-linux-aarch64.so.1` and the files in `fugaku-libs.txt`.
3. Compile the `hello-world` apps (using the `compile.sh` script) and copy them to the same host where you run the simulator.
4. In `riken_simulator` dir (asuming it is next to the `sim-container` dir)  run something like this

```
./build/ARM/gem5.opt ./configs/example/se.py \
	--cpu-type=O3_ARM_PostK_3 --caches --l2cache \
	-e ../sim-container/fj_env.txt -n 2 \
        -c ../sim-container/ld-linux-aarch64.so.1 \
        -o ../sim-container/hello-worlds/hello.fcc
```
