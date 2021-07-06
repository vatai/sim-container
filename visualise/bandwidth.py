#!/bin/env python
import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def read_df(path: Path):
    pattern = r".*numthreads(\d+)_bankbit(\d+)_buswidth(\d+)_respwidth(\d+).*"
    match = re.match(pattern, path.name)
    num_threads, bankbit, bus_width, resp_width = match.groups()
    data = dict(
        num_threads=int(num_threads),
        bankbit=int(bankbit),
        bus_width=int(bus_width),
        resp_width=int(resp_width),
    )
    data["config"] = f"{num_threads}-{bankbit}-{bus_width}-{resp_width}"
    with open(path) as file:
        for line in file.readlines():
            if " -s " in line:
                num_elems = line.split(" -s ")[1]
                data["num_elems"] = int(num_elems[:-2])
                continue
            split = line.split()
            if len(split) < 2:
                continue
            key = split[0]
            if key in ["Copy", "Mul", "Add", "Triad", "Dot"]:
                data[key.lower()] = float(split[1])

    # Function    MBytes/sec  Min (sec)   Max         Average
    # Copy        62296.578   0.00000     0.00000     0.00000
    # Mul         56529.040   0.00000     0.00000     0.00000
    # Add         84720.483   0.00000     0.00000     0.00000
    # Triad       80864.272   0.00000     0.00000     0.00000
    # Dot         26116.897   0.00001     0.00001     0.00001
    return pd.Series(data)


def read_dataframe(path: Path):
    paths = path.glob("*.stdout.txt")
    series = [read_df(path) for path in paths]
    df = pd.DataFrame(series)
    df = pd.pivot(
        df,
        index="num_elems",
        columns=["config"],
        values=["copy", "add", "mul", "triad", "dot"],
    )
    df = df.sort_index()
    # df.index = df.index.to_series().map(human_readable_size)
    return df


def human_readable_size(size, pos=None):
    size = float(size * 8)
    for suffix in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{int(size)}{suffix}"
        size /= 1024.0
    return f"{size}TB"


def plot(df, filename, show=False):
    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(human_readable_size)
    ax.yaxis.set_major_formatter(lambda t, p: f"{t/1024:0.04}GB/s")
    ax.set_title(filename + "\n{num_threads}-{bankbits}-{bus_width}-{resp_width}")
    df.plot(ax=ax)
    plt.savefig(filename, bbox_inches="tight")
    if show:
        plt.show()
    plt.cla()
    plt.clf()
    plt.close(fig)


def main():
    default_m5_path = Path("~/Sync/tmp/work/babel-bandwidth/m5").expanduser()
    parser = argparse.ArgumentParser()
    parser.add_argument("--m5-path", type=Path, default=default_m5_path)
    args = parser.parse_args()
    df = read_dataframe(args.m5_path)

    for key in ["copy", "add", "mul", "triad", "dot"]:
        plot(df[key], f"{key}-bandwidth")

    plot(df, "all", True)
    print("Done!")


main()
