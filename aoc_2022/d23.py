import sys
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Tuple

import helpers

Point = Tuple[int, int]
dial = ["N", "S", "W", "E"]
dial_rules: Dict[str, Tuple[str, str, str]] = {
    "N": ("N", "NE", "NW"),
    "S": ("S", "SE", "SW"),
    "W": ("W", "NW", "SW"),
    "E": ("E", "NE", "SE"),
}

compass: Dict[str, Point] = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
    "NW": (-1, -1),
}


def round(elves: List[Point], turn) -> Tuple[List[Point], int]:
    moves = moves_available(elves)
    movement_proposals = moves_proposed(moves, turn)

    movement_counter: Dict[Point, int] = defaultdict(int)
    bucket = {}
    for p1, data in movement_proposals.items():
        if len(data) < 4:
            p2: Point = compass[data[0]]
            p3 = p1[0] + p2[0], p1[1] + p2[1]
            bucket[p1] = p3
            movement_counter[p3] += 1

    final_positions = []
    for p1, p2 in bucket.items():
        if movement_counter[p2] == 1:
            final_positions.append(p2)
            elves.remove(p1)
    result = final_positions + elves

    return result, len(bucket)


def moves_proposed(moves, turn: int) -> Dict[Point, List[str]]:
    # If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
    # If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
    # If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
    # If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
    movement_proposals: Dict[Point, List[str]] = {}
    for p1, empties in moves.items():
        items = []
        for c in range(4):
            d = dial[(c + turn) % 4]
            rules = dial_rules[d]
            if all(rule in empties for rule in rules):
                items.append(d)
        if 0 < len(items) < 4:
            movement_proposals[p1] = items
    return movement_proposals


def moves_available(elves: List[Point]) -> Dict[Point, Dict[str, Point]]:
    moves = dict()
    for elf in elves:
        results = dict()
        for k, (y, x) in compass.items():
            new_row = elf[0] + y
            new_col = elf[1] + x
            if (new_row, new_col) not in elves:
                results[k] = (new_row, new_col)
        if results:
            # Only track moves if there are results
            moves[elf] = results
    return moves


def pprint(elves: List[Point], round: int, score: int) -> None:
    print(f"\n== End of Round [{round:02}] With A Score of [{score}] ==")
    row_min = min(e[0] for e in elves)
    row_max = max(e[0] for e in elves)
    col_min = min(e[1] for e in elves)
    col_max = max(e[1] for e in elves)
    for row in range(row_min, row_max + 1):
        line = ""
        for col in range(col_min, col_max + 1):
            if (row, col) in elves:
                line += "#"
            else:
                line += "."
        print(line)


def part01(elves: List[Point]) -> int:
    for count in range(10):
        elves, number_of_changes = round(elves, count)

    rows_ = [e[0] for e in elves]
    cols_ = [e[1] for e in elves]
    a = abs(min(rows_) - max(rows_)) + 1
    b = abs(min(cols_) - max(cols_)) + 1
    return (a * b) - len(elves)


def run() -> None:
    path = Path(__file__).parent / "data" / "day_23.txt"
    lines = helpers.lines(path)
    elves = []
    rows = [list(line) for line in lines]
    for row in range(len(rows)):
        for col in range(len(rows[0])):
            if rows[row][col] == "#":
                elves.append((row, col))

    assert part01(elves[::]) == 3871
    assert part02(elves[::]) == 925


def part02(elves: List[Point]) -> int:
    count = 0
    number_of_changes = sys.maxsize
    while number_of_changes > 0:
        elves, number_of_changes = round(elves, count)
        count += 1
    return count


if __name__ == "__main__":
    run()
