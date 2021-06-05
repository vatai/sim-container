#!/bin/env python
from pathlib import Path

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


def get_data(path="~/bali-sim-m5"):
    path = Path(path).expanduser()
    key = "host_seconds"
    for m5dir in path.glob("*.fccpx"):
        name = m5dir.name
        stats = get_stats_dict(m5dir)
        print(name, stats[key])


get_data()
