from pathlib import Path
from typing import List

import helpers


def part01(plays: List[List[str]]) -> int:
    decrypt = {
        "X": {"A": 3 + 1, "B": 0 + 1, "C": 6 + 1},  # Draw / Lose / Win + 1
        "Y": {"A": 6 + 2, "B": 3 + 2, "C": 0 + 2},  # Win / Draw / Lose + 2
        "Z": {"A": 0 + 3, "B": 6 + 3, "C": 3 + 3},  # Lose / Win / Draw + 3
    }

    return sum(decrypt[me][enemy] for (enemy, me) in plays)


def part02(plays: List[List[str]]) -> int:
    decrypt = {
        "X": {"A": 3 + 0, "B": 1 + 0, "C": 2 + 0},  # Lose + 0
        "Y": {"A": 1 + 3, "B": 2 + 3, "C": 3 + 3},  # Draw + 3
        "Z": {"A": 2 + 6, "B": 3 + 6, "C": 1 + 6},  # Win  + 6
    }

    return sum(decrypt[me][enemy] for (enemy, me) in plays)


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_02.txt")
    plays = [line.split() for line in lines]

    assert part01(plays) == 11666
    assert part02(plays) == 12767


if __name__ == "__main__":
    run()
