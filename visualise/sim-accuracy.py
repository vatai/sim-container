#!/bin/env python
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def get_stats_dict(m5dir):
    stats = m5dir / "stats.txt"
    result = list()
    with open(stats) as file:
        for line in file:
            pos = line.find("#")
            if pos >= 0:
                split = line[:pos].split()
                value = split[1:] if len(split) > 2 else split[1]
                result.append((split[0], value))
    return dict(result)


def get_stats_df(path):
    path = Path(path).expanduser()
    entries = {}
    for m5dir in path.glob("*.fccpx"):
        name = m5dir.name
        stats = get_stats_dict(m5dir)
        entries[name] = stats
    df = pd.DataFrame(entries).transpose()
    df["source"] = path
    return df


def host_seconds_barplot():
    bali_df = get_stats_df("~/bali-sim-m5")
    rsim_df = get_stats_df("~/riken-sim-m5")
    big_df = pd.concat([bali_df, rsim_df])
    key = "host_seconds"
    big_df[key] = pd.to_numeric(big_df[key])
    df = big_df.pivot(columns=["source"], values="host_seconds")

    print(df.head())
    df.plot.bar()
    plt.show()


def get_kernel_time(filename):
    with open(filename) as file:
        for line in file:
            try:
                return float(line)
            except Exception:
                pass


def get_kernel_times_df(path):
    path = Path(path).expanduser()
    files = path.glob("*.fccpx.stdout.txt")
    result = {}
    for filename in files:
        key = filename.name.split(".")[0]
        result[key] = get_kernel_time(filename)
    return pd.Series(result, name=path.name)


def main():
    a64fx = get_kernel_times_df("~/a64fx-outs")
    bali = get_kernel_times_df("~/bali-sim-m5")
    rsim = get_kernel_times_df("~/riken-sim-m5")

    sims = bali - rsim
    print(f"min: {sims.min()}, max: {sims.max()}")

    df = pd.DataFrame([bali, a64fx]).transpose()
    fig = plt.Figure()
    bar_plot = df.plot.bar()
    # plt.show()
    fig.savefig("bars", bbox_inches="tight")
    plt.close(fig)

    fast_a = a64fx >= bali
    slow_a = a64fx < bali
    positive = a64fx[fast_a] / bali[fast_a] - 1
    negative = bali[slow_a] / a64fx[slow_a] - 1
    combined = pd.concat([positive, -negative]).sort_index()

    fig = plt.Figure()
    speedup_plot = combined.plot.bar()
    # plt.show()
    fig.savefig("speedup", bbox_inches="tight")
    plt.close(fig)


main()
