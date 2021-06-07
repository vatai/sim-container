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
    df["source"] = path.name
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
    plt.close()


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


def accuracy_plot():
    a64fx = get_kernel_times_df("~/a64fx-outs")
    bali = get_kernel_times_df("~/bali-sim-m5")
    rsim = get_kernel_times_df("~/riken-sim-m5")
    abs_times = pd.DataFrame([bali, a64fx]).transpose().sort_index()

    fast_a = a64fx >= bali
    slow_a = a64fx < bali
    positive = a64fx[fast_a] / bali[fast_a] - 1
    negative = bali[slow_a] / a64fx[slow_a] - 1
    rel_times = pd.concat([positive, -negative]).sort_index()

    sims = bali - rsim
    print(f"min: {sims.min()}, max: {sims.max()}")

    # bar_plot = df.plot.bar()
    # fig = bar_plot.get_figure()
    # fig.savefig("bars", bbox_inches="tight")
    # plt.clf()

    # speedup_plot = rel_times.plot.bar()
    # fig = speedup_plot.get_figure()
    # fig.savefig("speedup", bbox_inches="tight")
    # plt.clf()

    rel_color = "green"
    dot_color = "lightgreen"
    fig, ax0 = plt.subplots()
    ax1 = ax0.twinx()

    ax0.set(
        title="Absolute and relative comparison of sim and chip \n"
        "of polybench benchmarks, only kernels, medium dataset, fccpx"
    )
    ax0.set_ylabel("Absolute speed (in seconds)")
    ax0.set_ylim(-0.05, 0.5)
    ax1.set_ylabel("Relative speed (+1: 2x speedup, -1: 2x slowdown)", color=rel_color)
    ax1.set_ylim(-0.22, 2.20)
    ax1.tick_params(axis="y", labelcolor=rel_color)

    abs_times.plot.bar(ax=ax0)
    rel_times.plot.line(marker="D", color=dot_color, linestyle="None", ax=ax1)
    ax1.axhline(linestyle="dashed", linewidth=1, color=rel_color)

    fig.tight_layout()
    # plt.show()
    plt.savefig("combined")
    plt.close()


host_seconds_barplot()
accuracy_plot()
