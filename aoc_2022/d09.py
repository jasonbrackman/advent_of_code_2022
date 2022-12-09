from copy import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple, Set

import helpers
from helpers import Pos


@dataclass
class RopeBridge:
    start: Pos  # row, col
    head: Pos
    tail: Pos
    visited: Set[Tuple[int, int]]
    tails: List[Pos] = field(default_factory=list)

    def set_tail_length(self, val: int) -> None:
        for _ in range(val):
            self.tails.append(copy(self.tail))

    def get_link_change(self, head: Pos, tail: Pos) -> Pos:
        distance = head.euclidean_distance(tail) >= 2
        col_d = head.col - tail.col
        row_d = head.row - tail.row

        if head.euclidean_distance(tail) >= 2:
            print()



    def pprint(self) -> None:
        for i in range(-13, 18, 1):
            cols = []
            for j in range(-13, 18, 1):
                if i == 0 and j == 0:
                    cols.append('S')
                else:
                    if self.head.row == i and self.head.col == j:
                        cols.append('H')
                    else:
                        stop = False
                        for index, t in enumerate(self.tails, 1):
                            if t.row == i and t.col == j:
                                cols.append(str(index))
                                stop = True
                        if not stop:
                            cols.append(' ')
            print('|'.join(cols))
        print("-" * 10)

    def move_tail(self, direction: str) -> None:
        # The tail can have an N length
        # The immediate portion of the tail closest to the head is always no less than one pos away
        # The tail can loop in on itself if length allows
        # The tail length
        if self.head.euclidean_distance(self.tail) >= 2:
            if direction == "R":
                self.tail.col += 1 if self.head.col > self.tail.col else -1
                self.tail.row = self.head.row
            elif direction == "L":
                self.tail.col += -1 if self.head.col < self.tail.col else 1
                self.tail.row = self.head.row
            elif direction == "U":
                self.tail.row += 1 if self.head.row > self.tail.row else -1
                self.tail.col = self.head.col
            elif direction == "D":
                self.tail.row += -1 if self.head.row < self.tail.row else 1
                self.tail.col = self.head.col

        if self.tail != self.tails[0]:
            # This indicates that tension was created -- the entire chain needs to be updated.
            self.tails.insert(0, copy(self.tail))
            self.tails.pop()

        self.visited.add((self.tails[-1].row, self.tails[-1].col))
        self.pprint()
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


def run():
    lines = helpers.lines(Path(__file__).parent / "data" / "day_09_test.txt")
    rules = []
    for line in lines:
        direction, count = line.split()
        rules.append((direction, int(count)))

    start, head, tail, visited = (
        Pos(0, 0),
        Pos(0, 0),
        Pos(0, 0),
        {
            (0, 0),
        },
    )
    rb = RopeBridge(start, head, tail, visited)
    rb.set_tail_length(9)
    for rule in rules:
        rb.move(rule)
        # rb.pprint()

    print(len(rb.visited)) #no 2176


if __name__ == "__main__":
    run()
