#!/usr/bin/env python
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def shorten_key(key):
    new_key = key[4:-15]
    # print(key)
    # print(new_key)
    return new_key


def get_cpu_times(path):
    times = json.load(open(path))
    times_short_names = {shorten_key(k): v for k, v in times.items()}
    return pd.DataFrame(times_short_names)


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


def get_sim_times(cpu_str, path):
    # old: m5out/polybenchmark/simparams/output.txt
    # new: m5out/params/polybenchmark/output.txt
    result = dict()
    for dir_params in list(path.glob("*")):
        key = shorten_key("bin" + str(dir_params).replace(str(path), ""))
        stats_path = dir_params / "stats.txt"
        if stats_path.exists():
            result[key] = stats_to_dict(stats_path)
        output_path = dir_params / "output.txt"
        if stats_path.exists():
            result[key][f"{cpu_str}_output_time"] = output_to_time(output_path)
    return pd.DataFrame(result)


def main():
    cpu_path = Path("../all_times.json")
    postk_path = Path("../m5out/cpuO3_ARM_PostK_3--l2size8MB--cacheline256")
    gem5_path = Path("../m5out/cpuHPI--l2size8MB--cacheline128")
    # sim_path = Path("../m5out.bak")

    cpu_times = get_cpu_times(cpu_path)
    postk_times = get_sim_times("postk", postk_path)
    gem5_times = get_sim_times("gem5", gem5_path)

    times = pd.concat([cpu_times, postk_times, gem5_times])
    print(times)

    # times = times.transpose()
    # time_mean_var = times.loc[:, ["output_time", "mean", "var"]]
    # time_mean_var.plot.box()
    # times.loc[["output_time"], :].plot()
    times = times.transpose()
    times = times[["postk_output_time", "gem5_output_time", "minimum"]]
    print(times)
    times = times.rename(
        columns={
            "postk_output_time": "postk_time",
            "gem5_output_time": "gem5_time",
            "minimum": "a64fx",
        }
    )
    times.plot.bar()

    plot_name = "postk-vs-gem5-vs-a64fx"
    plt.savefig(f"{plot_name}.png", bbox_inches="tight")
    plt.savefig(f"{plot_name}.pdf", bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
