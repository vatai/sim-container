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


def to_keyvalue_pairs(dict_with_list_values, key, benchmark):
    list_of_lists = [make_list(k, v) for k, v in dict_with_list_values.items()]
    if key:
        list_of_lists.append([(key, benchmark)])
    return list(itertools.product(*list_of_lists))


def get_params(d, k=None):
    tmp = map(lambda s: list(s.items())[0], d)
    return itertools.chain.from_iterable([to_keyvalue_pairs(d, k, b) for b, d in tmp])


def expand_configs_dict(configs_dict):
    sim_dict = configs_dict.pop("sim_params")
    sim_params = get_params(sim_dict)

    benchmark_dict = configs_dict.pop("benchmark")
    benchmark_params = get_params(benchmark_dict, "BENCHMARK")

    assert configs_dict == {}, "Incorrect yaml file"

    prod = itertools.product(benchmark_params, sim_params)
    # return list(map(" ".join, prod))

    # WARNING: do not remove the list conversion, because it will
    # return an iterator, which "disappears" after one use.
    return list(map(lambda t: t[0] + t[1], prod))


def launch_on_all_cores(cmd, configs):
    with concurrent.futures.ProcessPoolExecutor() as ex:
        home = {"HOME": os.path.expanduser("~")}
        futures = {ex.submit(run, cmd, env={**c, **home}): c for c in configs}
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


def main(args):
    configs_dict = yaml.load(open(args.path), Loader=yaml.SafeLoader)
    configs = expand_configs_dict(configs_dict)
    for i, c in enumerate(configs):
        print(i, c)
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
