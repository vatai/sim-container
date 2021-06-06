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


def get_stats_dict(path):
    path = Path(path).expanduser()
    entries = {}
    for m5dir in path.glob("*.fccpx"):
        name = m5dir.name
        stats = get_stats_dict(m5dir)
        entries[name] = stats
    df = pd.DataFrame(entries).transpose()
    df["source"] = path
    return df


def main():
    bali_df = get_stats_dict("~/bali-sim-m5")
    rsim_df = get_stats_dict("~/riken-sim-m5")
    big_df = pd.concat([bali_df, rsim_df])
    key = "host_seconds"
    big_df[key] = pd.to_numeric(big_df[key])
    df = big_df.pivot(columns=["source"], values="host_seconds")

    print(df.head())
    df.plot.bar()
    plt.show()


main()
