from typing import List, Tuple, Dict
import re
import helpers
from pathlib import Path

PATTERN_INT = re.compile(r"[-\d]+")
PATTERN_STR = re.compile(r"[A-Z]")


class Board:
    FACING = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self) -> None:
        self.rows: List[List[str]] = []
        self.width = 0
        self.height = 0
        self._arrow = 3
        self.current = (0, 0)

    def load(self, lines: List[List[str]]) -> None:
        max_len = max(len(line) for line in lines)
        for index, line in enumerate(lines):
            line += list(" " * (max_len - len(line)))
        self.rows = lines
        self.width = len(self.rows[0])
        self.height = len(self.rows)
        self.current = self._starting_pos()

    def spin(self, instructions: List[Tuple[str, int]]) -> int:
        result = -1
        for (i, steps) in instructions:
            self._arrow += -1 if i == "L" else 1
            result = self._move(steps)

        return result

    def _move(self, steps: int) -> int:
        move = Board.FACING[self._arrow % 4]
        row, col = self.current

        for _ in range(steps):
            counter = 1
            row = (row + move[0]) % self.height
            col = (col + move[1]) % self.width
            while self.rows[row][col] not in ".#":
                counter += 1
                row = (row + move[0]) % self.height
                col = (col + move[1]) % self.width

            if self.rows[row][col] == "#":
                row = (row - (move[0] * counter)) % self.height
                col = (col - (move[1] * counter)) % self.width

        self.current = (row, col)
        return 1000 * (row + 1) + 4 * (col + 1) + (self._arrow % 4)

    def _starting_pos(self) -> Tuple[int, int]:
        for row in range(len(self.rows)):
            for col in range(len(self.rows[row])):
                if self.rows[row][col] == ".":
                    return row, col


def parse() -> Tuple[List[List[str]], List[Tuple[str, int]]]:
    path = Path(__file__).parent / "data" / "day_22.txt"
    lines = []
    instructions = []

    skip = False
    for line in helpers.lines_no_strip(path):
        line = line.strip("\n")
        if line == "":
            skip = True
            continue

        if skip is False:
            lines.append(list(line))
        else:
            nums = re.findall(PATTERN_INT, line)
            inst = ["R"] + re.findall(PATTERN_STR, line)
            instructions = [(i, int(n)) for i, n in zip(inst, nums)]

    return lines, instructions


def part01(lines, instructions) -> None:
    board = Board()
    board.load(lines)
    p1 = board.spin(instructions)
    assert p1 == 65368


def run() -> None:
    lines, instructions = parse()
    part01(lines, instructions)


if __name__ == "__main__":
    run()
