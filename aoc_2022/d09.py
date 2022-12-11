from pathlib import Path
from typing import List, Tuple, Set

import helpers
from helpers import Pos


class RopeBridge:
    def __init__(self) -> None:
        self.head = Pos(0, 0)
        self.tail = Pos(0, 0)
        self.visited: Set[Tuple[int, int]] = {
            (0, 0),
        }
        self.tails: List[Pos] = []

    def set_tail_length(self, val: int) -> None:
        for _ in range(val):
            self.tails.append(Pos(0, 0))

    def move_tail(self, direction: str) -> None:
        head = self.head
        for tail in self.tails:
            stretched = head.euclidean_distance(tail) >= 2
            if stretched and head.row == tail.row:
                tail.col += 1 if head.col > tail.col else -1

            if stretched and head.col == tail.col:
                tail.row += 1 if head.row > tail.row else -1

            if head.euclidean_distance(tail) > 2:
                if tail.row != head.row:
                    tail.row += 1 if head.row > tail.row else -1

                if tail.col != head.col:
                    tail.col += 1 if head.col > tail.col else -1

            head = tail  # will exit with the last part of the tail

        self.visited.add((head.row, head.col))

    def move(self, rule: Tuple[str, int]) -> None:
        direction, count = rule
        if direction == "R":
            for index in range(count):
                self.head.col += 1
                self.move_tail(direction)
        elif direction == "L":
            for index in range(count):
                self.head.col += -1
                self.move_tail(direction)
        elif direction == "U":
            for index in range(count):
                self.head.row += -1
                self.move_tail(direction)
        elif direction == "D":
            for index in range(count):
                self.head.row += 1
                self.move_tail(direction)


def work(rules: List[Tuple[str, int]], tail_length: int) -> int:
    # Part1
    rb = RopeBridge()
    rb.set_tail_length(tail_length)
    for rule in rules:
        rb.move(rule)
    return len(rb.visited)


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_09.txt")
    rules = []
    for line in lines:
        direction, count = line.split()
        rules.append((direction, int(count)))
    assert work(rules, 1) == 6464
    assert work(rules, 9) == 2604  # not 2611 or 2621 ??


if __name__ == "__main__":
    run()
