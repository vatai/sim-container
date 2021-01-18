#!/usr/bin/env python
import json
import os
from pathlib import Path

import pandas


def get_cpu_times(path):
    times = json.load(open(path))
    return times


def stats_to_dict(path):
    result = dict()
    for line in open(path):
        fields = line.split()
        if "#" in fields:
            pos = fields.index("#")
            fields = fields[:pos]
            key = fields[0]
            value = fields[1] if len(fields) == 2 else fields[1:]
            result[key] = value
    return result


def output_to_time(path):
    with open(path) as file:
        lines = file.readlines()
        return float(lines[-2])


def get_sim_times(path):
    result = dict()
    for dir_path in path.glob("*"):
        key = "bin" + str(dir_path).replace(str(path), "")
        for base in list(dir_path.glob("*")):
            stats_path = base / "stats.txt"
            if stats_path.exists():
                result[key] = stats_to_dict(stats_path)
            output_path = base / "output.txt"
            if stats_path.exists():
                result[key]["output_time"] = output_to_time(output_path)
    return result


def main():
    cpu_path = Path("../all_times.json")
    sim_path = Path(os.path.expanduser("../m5out"))

    cpu_times = get_cpu_times(cpu_path)
    cpu_times = pandas.DataFrame(cpu_times).transpose()

    sim_times = get_sim_times(sim_path)
    sim_times = pandas.DataFrame(sim_times).transpose()

    key = "bin/heat-3d-MEDIUM_DATASET"


# if __name__ == "__main__":
main()
