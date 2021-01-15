import os
import sys

import numpy as np


def get_run_times(executable, num_repeat):
    run_times = []
    for i in range(num_repeat):
        stream = os.popen(executable)
        time = float(stream.read())
        run_times.append(time)
    run_times = np.array(run_times)
    return run_times


def main():
    assert len(sys.argv) > 1, "Specify the executable as a parameter"
    executable = sys.argv[1]

    num_repeat = 50
    if len(sys.argv) > 2:
        num_repeat = int(sys.argv[2])

    run_times = get_run_times(executable, num_repeat)

    print(f"{executable:20} mean: {run_times.mean():10f} var: {run_times.var():7}")
    with open(f"{executable}.runtimes.txt", "w") as file:
        file.write(str(run_times))


if __name__ == "__main__":
    main()
