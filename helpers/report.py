import time
from types import FunctionType
from typing import List


def time_it(command: FunctionType) -> None:
    t1 = time.perf_counter()
    command()
    print(
        f"[{str(command.__module__)}.{command.__name__}]: Completed in {(time.perf_counter() - t1) * 1_000:0.1f} ms"
    )


def time_it_all(args: List) -> None:
    for arg in args:
        time_it(arg)

