## Riken simulator with `docker`

### Build image

Get the `riken.docker` file and run the following command:

```
docker build \
    --build-arg USER=$(id -un) \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP=$(id -gn) \
    --build-arg GROUP_ID=$(id -g) \
    -t riken/simulator .
```

Note the dot `.` at the end!  This creates the docker image
`riken/simulator`.

### Run image

To run the `riken/simulator` docker image, run the following command:

```
HOST $ docker run -it \
  -v "$(pwd)":/hostdir \
  -w /home/user \
  riken/simulator \
  /bin/bash \
```

This creates a container which is a running instance of the
`riken/simulator` image and runs `bash` inside this container.  It
will also mount/bind the current directory (`"$(pwd)`) on the host, to
the `/hostdir` in the container.  `/hostdir` is read-only in the
container.  To copy files from the container to the host you can use
the `docker cp` command e.g.
```
HOST $ docker cp <container_name>:/abs/path/tosomefile.txt .
```

Each container (i.e. running instance of the image) has a name.  These
name can be listed using the `docker container ls -a` command (which
include both running and inactive containers).

Docker usually generates silly names for containers, such as:
`stupefied_johnson`.

To clean up, you
should run `docker container prune` once in a while.

## Inside the container

The docker image has the RIKEN-Simulator ready inside
`${HOME}/riken_simulator`.  To compile a program to be run by the
simulator use `aarch64-linux-gnu-gcc-8 -static`.

### Example project
1. Copy the the `dot_prod` project from the host's current directory
   to your homedir in the container: `~/dot_prod`.
2. Compile `~/dot_prod/main`
3. Run the simulation.

```
cp -r /hostdir/dot_prod ~/
make -C ~/dot_prod
~/riken_simulator/util/gem5-o3 -c ~/dot_prod/main
```
