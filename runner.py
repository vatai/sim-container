#!/bin/env python

import argparse
import concurrent.futures
import itertools
import os
from pathlib import Path
from subprocess import run

import yaml

COMPILE_CMD = "./02-compile-benchmark.sh"
SIM_CMD = "./03-run-benchmark.sh"


def make_pair(a, b):
    # return f'{a.upper()}="{b}"'
    return a.upper(), b


def make_list(k, v):
    if isinstance(v, str):
        if Path(v).exists():
            with open(v) as f:
                lines = f.readlines()
            lines = filter(lambda t: t[0] != "#", lines)
            return [(k, i.strip()) for i in lines]
        else:
            return [(k, v)]
    elif isinstance(v, list):
        return [(k, i) for i in v]
    else:
        raise ValueError


def fun2(t):
    return [make_list(k, v) for k, v in t]


def fun1(t):
    return list(itertools.product(*fun2(t)))


def get_sim_params(d):
    tmp = sum([fun1(t.items()) for t in d], [])
    for t in tmp:
        # print("-", list(map(lambda t: make_pair(*t), t)))
        print("-", t)
    return tmp


def fun4(k, v):
    tmp = get_sim_params(v)
    return list(map(lambda t: (("BENCHMARK", k), *t), tmp))


def fun3(t):
    return sum([fun4(k, v) for k, v in t.items()], [])


def expand_configs_dict(configs_dict):
    benchmark_dict = configs_dict.pop("benchmark")
    benchmark_params = [
        {"BENCHMARK": "polybench.source"},
        {"BENCHMARK": "xsbench.source", "dataset": "mini"},
        {"BENCHMARK": "xsbench.source", "dataset": "small"},
    ]
    sim_dict = configs_dict.pop("sim_params")
    sim_params = [
        {"CACHELINE": "128", "CACHE_SIZE": "8MB"},
        {"CACHELINE": "128", "CACHE_SIZE": "1MB"},
    ]
    get_sim_params(sim_dict)
    tmp = sum([fun3(t) for t in benchmark_dict], [])
    for t in tmp:
        print("*", t)

    assert configs_dict == {}, "Incorrect yaml file"

    prod = itertools.product(benchmark_params, sim_params)
    # return list(map(" ".join, prod))

    # WARNING: do not remove the list conversion, because it will
    # return an iterator, which "disappears" after one use.
    return list(map(lambda t: t[0] | t[1], prod))


def launch_on_all_cores(cmd, configs):
    with concurrent.futures.ProcessPoolExecutor() as ex:
        home = {"HOME": os.path.expanduser("~")}
        futures = {ex.submit(run, cmd, env={**c, **home}): c for c in configs}
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


def main(args):
    configs_dict = yaml.load(open(args.path), Loader=yaml.SafeLoader)
    configs = expand_configs_dict(configs_dict)
    if args.compile:
        launch_on_all_cores(COMPILE_CMD, configs)
    if args.runsim:
        launch_on_all_cores(SIM_CMD, configs)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        type=str,
        help="Path to the yaml file",
    )
    parser.add_argument(
        "--compile",
        type=bool,
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Flag to enable/disable the compilation",
    )
    parser.add_argument(
        "--runsim",
        type=bool,
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Flag to enable/disable the simulation",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    main(args)
