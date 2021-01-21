#!/usr/bin/env python
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas


def shorten_key(key):
    new_key = key[4:-15]
    # print(key)
    # print(new_key)
    return new_key


def get_cpu_times(path):
    times = json.load(open(path))
    return {shorten_key(k): v for k, v in times.items()}


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
        key = shorten_key(key)
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
    cpu_times = pandas.DataFrame(cpu_times)  # .transpose()

    sim_times = get_sim_times(sim_path)
    sim_times = pandas.DataFrame(sim_times)  # .transpose()

    times = pandas.concat([cpu_times, sim_times])

    # times = times.transpose()
    # time_mean_var = times.loc[:, ["output_time", "mean", "var"]]
    # time_mean_var.plot.box()
    # times.loc[["output_time"], :].plot()
    times = times.transpose()
    times = times[["output_time", "minimum"]]
    times = times.rename(columns={"output_time": "sim_time", "minimum": "a64fx"})
    times.plot.bar()
    plt.show()


if __name__ == "__main__":
    main()
