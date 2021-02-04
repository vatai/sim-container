#!/bin/env python

import argparse
import concurrent.futures
import itertools
import os
import subprocess
from pathlib import Path

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
            return [make_pair(k, i.strip()) for i in lines]
        else:
            return [make_pair(k, v)]
    elif isinstance(v, list):
        return [make_pair(k, i) for i in v]
    else:
        raise ValueError


def expand_configs_dict(configs_dict):
    bench = [make_pair("bench", configs_dict.pop("bench"))]

    sim_dict = configs_dict.pop("sim_params").items()
    sim_params = [make_list(k, v) for k, v in sim_dict]

    bench_dict = configs_dict.pop("bench_params").items()
    bench_params = [make_list(k, v) for k, v in bench_dict]

    assert configs_dict == {}, "Incorrect yaml file"

    prod = itertools.product(*sim_params, bench, *bench_params)
    # return list(map(" ".join, prod))

    # WARNING: do not remove the list conversion, because it will
    # return an iterator, which "disappears" after one use.
    return list(map(dict, prod))


def launch_on_all_cores(cmd, configs):
    with concurrent.futures.ProcessPoolExecutor() as ex:
        run = subprocess.run
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
