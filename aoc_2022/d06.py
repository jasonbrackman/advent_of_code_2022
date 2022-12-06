from pathlib import Path
from typing import Optional

import helpers


def part(line: str, window: int) -> Optional[int]:
    for index in range(len(line)):
        if len(set(line[index : index + window])) == window:
            return index + window
    return None


def run() -> None:
    line = helpers.lines(Path(__file__).parent / "data" / "day_06.txt")[0]
    assert part(line, 4) == 1100
    assert part(line, 14) == 2421


if __name__ == "__main__":
    run()
