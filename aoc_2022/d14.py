import copy
import re
from pathlib import Path
from typing import List, Tuple, Set

import helpers

PATTERN = re.compile(r"[0-9]+")


class Waterfall:
    def __init__(self) -> None:
        self.rocks: Set[Tuple[int, int]] = set()
        self.sand: Set[Tuple[int, int]] = set()
        self.tick = 0
        self.lowest = -2
        self.start = (500, 0)
        self.floor = -2

    def break_rocks(self, rocks: List[List[List[int]]]) -> None:
        for (r1, r2) in rocks:
            p1x, p1y = r1
            p2x, p2y = r2

            for x in range(min(p1x, p2x), max(p1x, p2x) + 1):
                for y in range(min(p1y, p2y), max(p1y, p2y) + 1):
                    self.rocks.add((x, y))

        self.lowest_rock()
        self.floor = self.lowest + 2

    def lowest_rock(self) -> None:
        self.lowest = max(j for (i, j) in self.rocks)

    def blocked(self, pos: Tuple[int, int]) -> bool:
        if pos in self.rocks:
            return True
        if pos in self.sand:
            return True
        if pos[1] == self.floor:
            return True
        return False

    def drop(self, test_lowest=False) -> int:
        pos = self.start

        while True:
            left = pos[0] - 1
            right = pos[0] + 1
            down = pos[1] + 1

            if test_lowest:
                if down > self.lowest:
                    # we have fallen off the edge of the earth
                    return len(self.sand)

            if not self.blocked((pos[0], down)):
                pos = (pos[0], down)
            else:
                # blocked so now what?
                if not self.blocked((left, down)):
                    pos = (left, down)
                elif not self.blocked((right, down)):
                    pos = (right, down)
                else:
                    # we are now blocked on both sides and at rest
                    self.sand.add(pos)
                    if pos == self.start:
                        return len(self.sand)
                    # start again
                    pos = self.start

                    # for some debug/fun
                    # self.pprint()

    def pprint(self) -> None:
        for x in range(0, self.floor + 1):
            for y in range(450, 550):
                pos = (y, x)
                if pos == (0, 500):
                    print("+", end="")
                elif pos in self.sand:
                    print("o", end="")
                elif pos in self.rocks:
                    print("#", end="")
                elif pos[1] == self.floor:
                    print("F", end="")
                else:
                    print(".", end="")
            print()


def get_rock_rules() -> List[List[List[int]]]:
    rock_rules = []

    path = Path(__file__).parent / "data" / "day_14.txt"
    lines = helpers.lines(path)

    for line in lines:
        nums = [int(i) for i in re.findall(PATTERN, line)]
        pairs = []
        for item in [nums[index : index + 2] for index in range(0, len(nums), 2)]:
            pairs.append(item)
            if len(pairs) == 2:
                rock_rules.append(copy.deepcopy(pairs))
                pairs.pop(0)
    return rock_rules


def run() -> None:
    rocks = get_rock_rules()
    wf = Waterfall()
    wf.break_rocks(rocks)
    assert wf.drop(test_lowest=True) == 745
    assert wf.drop() == 27551


if __name__ == "__main__":
    run()
