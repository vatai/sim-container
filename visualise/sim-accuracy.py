#!/bin/env python
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


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


def get_stats_df(path, m5dir_glob="*.fccpx"):
    entries = {}
    for m5dir in path.glob(m5dir_glob):
        name = m5dir.name.replace("omp-stream10_-s_262144_numthreads", "")
        try:
            name = int(name)
            name = f"{name:03}"
        except Exception:
            pass
        if not m5dir.is_dir():
            continue
        stats = get_stats_dict(m5dir)
        entries[name] = stats
    df = pd.DataFrame(entries).transpose()
    return df.sort_index()


def get_kernel_time(filename):
    with open(filename) as file:
        for line in file:
            try:
                return float(line)
            except Exception:
                pass


def get_kernel_times_df(path, stdout_glob="*.fccpx.stdout.txt"):
    files = path.glob(stdout_glob)
    result = {}
    for filename in files:
        key = ".".join(filename.name.split(".")[:3])
        result[key] = get_kernel_time(filename)
    wtime = pd.Series(result, name="kernel_wtime", dtype=float)
    df = pd.DataFrame(wtime)
    return df.sort_index()


def get_rel_abs_times(df, source1, key1, source2=None, key2=None):
    source2 = source2 if source2 else source1
    key2 = key2 if key2 else key1
    data1 = df.loc[df["source"] == source1, key1].astype(float)
    data2 = df.loc[df["source"] == source2, key2].astype(float)
    assert source1 == source2 or key1 == key2
    if source1 == source2:
        data1.name = key1
        data2.name = key2
    else:
        data1.name = source1
        data2.name = source2
    data1.index = data1.index.str.split(".").str[0]
    data2.index = data2.index.str.split(".").str[0]
    fast1 = data1 >= data2
    fast2 = data1 < data2
    positive = data2[fast2] / data1[fast2] - 1
    negative = data1[fast1] / data2[fast1] - 1
    rel_times = pd.concat([positive, -negative]).sort_index()
    abs_times = pd.DataFrame([data2, data1]).transpose().sort_index()
    return rel_times, abs_times


def speedup_plot(title, savefig, rel_times, abs_times):
    rel_color = "green"
    dot_color = "lightgreen"
    fig, ax0 = plt.subplots()
    ax1 = ax0.twinx()

    margin = 1.3
    top1 = max(rel_times) * margin
    bot1 = min(rel_times) * margin
    top0 = abs_times.max()[0] * margin
    bot0 = min(0, top0 * bot1 / top1)
    ax0.set(title=title)
    ax0.set_ylabel("Absolute speed (in seconds)")
    ax0.set_ylim(bot0, top0)
    ax1.set_ylabel("Relative speed (+1: 2x speedup, -1: 2x slowdown)", color=rel_color)
    ax1.set_ylim(bot1, top1)
    ax1.tick_params(axis="y", labelcolor=rel_color)

    abs_times.plot.bar(ax=ax0)
    rel_times.plot.line(marker="D", color=dot_color, linestyle="None", ax=ax1)
    ax1.axhline(linestyle="dashed", linewidth=1, color=rel_color)
    gmean = stats.gmean(rel_times.abs())
    ax1.axhline(gmean, linestyle="dotted", color=rel_color)
    ax1.text(
        1.0,
        gmean,
        f"gemea: {gmean:0.06}",
        va="center",
        color=rel_color,
        backgroundcolor="w",
    )

    fig.tight_layout()
    plt.savefig(savefig)
    plt.show()
    plt.close()


def get_polybench_host_seconds_wtime_df(m5dir):
    m5dir = Path(m5dir).expanduser()
    assert m5dir.exists()
    df1 = get_stats_df(m5dir)
    df2 = get_kernel_times_df(m5dir)
    df = pd.concat([df1, df2], axis=1)
    df["source"] = m5dir.name
    return df


def get_ompstream_host_sim_seconds_df(m5dir):
    m5dir = Path(m5dir).expanduser()
    assert m5dir.exists()
    df1 = get_stats_df(m5dir, "*")
    df2 = get_kernel_times_df(m5dir)
    df = pd.concat([df1, df2], axis=1)
    df["source"] = m5dir.name
    return df


def main():
    root = "."
    poly_dirs = [
        f"{root}/bali-sim-m5",
        f"{root}/riken-sim-m5",
        f"{root}/a64fx-outs",
    ]
    poly_dfs = list(map(get_polybench_host_seconds_wtime_df, poly_dirs))
    ompstream_dfs = [get_ompstream_host_sim_seconds_df(f"{root}/omp-stream")]
    df = pd.concat(ompstream_dfs + poly_dfs)

    title = "Simulation accuracy: chip vs sim kernel wtime"
    times = get_rel_abs_times(df, "bali-sim-m5", "kernel_wtime", "a64fx-outs")
    speedup_plot(title, "sim_accuracy.pdf", *times)

    title = "Simulation slowdown"
    times = get_rel_abs_times(df, "bali-sim-m5", "sim_seconds", key2="host_seconds")
    speedup_plot(title, "sim_slowdown.pdf", *times)

    title = "Full vs kernel wtime (on sim)"
    times = get_rel_abs_times(df, "bali-sim-m5", "kernel_wtime", key2="sim_seconds")
    speedup_plot(title, "kernel_ratio.pdf", *times)

    title = "Simulation slowdown"
    times = get_rel_abs_times(df, "omp-stream", "sim_seconds", key2="host_seconds")
    speedup_plot(title, "sim_slowdown_omp.pdf", *times)

    print("DONE")


# if __name__ == "__main__":
main()
