from typing import List

import helpers
from pathlib import Path

snafu = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def snafu_to_decimal(line: str) -> int:
    t = 0
    for i, val in enumerate(reversed(list(line))):
        current_max = 1
        if i > 0:
            current_max = 5**i
        t += snafu[val] * current_max
    return t


def decimal_to_snafu(val: int) -> str:
    # print(f"Starting with: {val}")
    result = ""

    cache = {i: 5**i for i in range(40)}
    cache[0] = 1

    i = 0

    chain = None
    while val != 0:
        mv = sum(cache[r] for r in cache if r <= i)
        mv_minus = sum(cache[r] for r in cache if r < i)
        max_val = 1 if mv == 0 else mv

        if val > 0:
            if val <= (max_val + max_val):
                if val <= (mv + mv_minus):
                    if chain is not None and abs(i - chain) > 1:
                        result += "0" * (abs(i - chain) - 1)
                    result += "1"
                    val -= cache[i]

                else:
                    if chain is not None and abs(i - chain) > 1:
                        result += "0" * (abs(i - chain) - 1)
                    result += "2"
                    val -= cache[i] + cache[i]

                if val == 0:
                    for _ in range(i):
                        result += "0"

                chain = i
                i = 0
            else:
                i += 1

        elif val < 0:
            if val >= (max_val + max_val) * -1:
                if val >= (mv + mv_minus) * -1:
                    if chain is not None and abs(i - chain) > 1:
                        result += "0" * (abs(i - chain) - 1)
                    result += "-"
                    val += cache[i]
                else:
                    if chain is not None and abs(i - chain) > 1:
                        result += "0" * (abs(i - chain) - 1)
                    result += "="
                    val += cache[i] + cache[i]

                if val == 0:
                    for _ in range(i):
                        result += "0"
                chain = i
                i = 0
            else:
                i += 1

    return result


def run() -> None:
    path = Path(__file__).parent / "data" / "day_25.txt"
    lines = helpers.lines(path)
    collections = [snafu_to_decimal(line) for line in lines]
    new_val = sum(collections)
    assert decimal_to_snafu(new_val) == "122-12==0-01=00-0=02"


def run_tests() -> None:
    x = (
        ("1=-0-2", 1747),
        ("12111", 906),
        ("2=0=", 198),
        ("21", 11),
        ("2=01", 201),
        ("111", 31),
        ("20012", 1257),
        ("112", 32),
        ("1=-1=", 353),
        ("1-12", 107),
        ("12", 7),
        ("1=", 3),
        ("122", 37),
    )
    for i, j in x:
        assert snafu_to_decimal(i) == j
        assert decimal_to_snafu(j) == i, f"{decimal_to_snafu(j)}, {i}"


if __name__ == "__main__":
    run()
