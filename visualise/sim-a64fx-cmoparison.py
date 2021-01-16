#!/usr/bin/env python
import json
import os
from pathlib import Path

import pandas


def get_cpu_times(path):
    times = json.load(open(path))
    # @todo(vatai): Do this in output generation and remove this
    # conversion.
    times = dict([tuple(*t.items()) for t in times])
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


def get_sim_times(path):
    result = dict()
    for dir_path in path.glob("*"):
        key = "bin" + str(dir_path).replace(str(path), "")
        for base in list(dir_path.glob("*")):
            stats_path = base / "stats.txt"
            if stats_path.exists():
                result[key] = stats_to_dict(stats_path)
    return result


def main():
    cpu_path = Path("../all_times.json")
    sim_path = Path(os.path.expanduser("~/allm5"))
    cpu_times = get_cpu_times(cpu_path)
    sim_times = get_sim_times(sim_path)
    # print(list(cpu_times.keys()))
    print(list(sim_times.values()))


# if __name__ == "__main__":
main()
