#!/bin/env python

import itertools
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import yaml


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
    return map(dict, prod)


def main(path):
    configs_dict = yaml.load(open(path), Loader=yaml.SafeLoader)
    configs = expand_configs_dict(configs_dict)
    print(list(configs))
    # with ProcessPoolExecutor() as executor:
    #     print(executor._max_workers)


main("./polybench-test.yaml")
