from pathlib import Path
from string import ascii_letters
from typing import List

import helpers


def part01(lines: List[str]) -> int:
    total = 0
    for line in lines:
        half_length = len(line) // 2
        result = max(set(line[:half_length]).intersection(set(line[half_length:])))
        total += ascii_letters.index(result) + 1
    return total


def part02(lines: List[str]) -> int:
    step = 3
    total = 0
    for x in range(0, len(lines), step):
        group = [set(g) for g in lines[x : x + step]]
        result = group[0].intersection(group[1]).intersection(group[2]).pop()
        total += ascii_letters.index(result) + 1

    return total


def run() -> None:
    """Run all the parts for timing purposes."""
    lines = helpers.lines(Path(__file__).parent / 'data' / 'day_03.txt')
    assert part01(lines) == 7872
    assert part02(lines) == 2497


if __name__ == "__main__":
    run()
