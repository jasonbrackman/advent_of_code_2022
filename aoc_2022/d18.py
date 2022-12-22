from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import List, Set, Tuple, Callable

from helpers import lines

PATTERN = re.compile(r"^(10+)?1")


class Cube:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.n: Set[Tuple[int, int, int]] = set()
        self.i: Set[Tuple[int, int, int]] = set()
        self.c: Set[Tuple[int, int, int]] = set()

        self.max_x: int = -1
        self.max_y: int = -1
        self.max_z: int = -1
        self.min_x: int = -1
        self.min_y: int = -1
        self.min_z: int = -1

    def setup(self, cubes: List[Cube]) -> None:
        self.c = {(c.x, c.y, c.z) for c in cubes}
        self.max_x = max(x for (x, y, z) in self.c)
        self.max_y = max(y for (x, y, z) in self.c)
        self.max_z = max(z for (x, y, z) in self.c)
        self.min_x = min(x for (x, y, z) in self.c)
        self.min_y = min(y for (x, y, z) in self.c)
        self.min_z = min(z for (x, y, z) in self.c)
        self.neighbours()
        self.internals()

    def num_faces(self) -> int:
        max_faces = 6
        return max_faces - len(self.n)

    def is_internal(self) -> List[Tuple[int, int, int]]:
        results = []

        # x

        sub_x = self.x - 1
        if sub_x >= self.min_x:
            pos = (sub_x, self.y, self.z)
            if pos not in self.c:
                results.append(pos)

        add_x = self.x + 1
        if add_x <= self.max_x:
            pos = (add_x, self.y, self.z)
            if pos not in self.c:
                results.append(pos)

        # y
        sub_y = self.y - 1
        if sub_y >= self.min_y:
            pos = (self.x, sub_y, self.z)
            if pos not in self.c:
                results.append(pos)

        add_y = self.y + 1
        if add_y <= self.max_y:
            pos = (self.x, add_y, self.z)
            if pos not in self.c:
                results.append(pos)

        # z
        sub_z = self.z - 1
        if sub_z >= self.min_z:
            pos = (self.x, self.y, sub_z)
            if pos not in self.c:
                results.append(pos)

        add_z = self.z + 1
        if add_z <= self.max_z:
            pos = (self.x, self.y, add_z)
            if pos not in self.c:
                results.append(pos)

        return results

    def _touching(self, x: int, y: int, z: int) -> int:
        return int(abs(self.x - x) + abs(self.y - y) + abs(self.z - z))

    def neighbours(self) -> None:
        self.n = {(x, y, z) for (x, y, z) in self.c if self._touching(x, y, z) == 1}

    def internals(self) -> None:
        # x
        for index in range(self.max_x):
            tests = [(self.x - index, self.y, self.z), (self.x + index, self.y, self.z)]
            for (x, y, z) in tests:
                if self.min_x <= x <= self.max_x:
                    if (x, y, z) not in self.c:
                        self.i.add((x, y, z))

        # y
        for index in range(self.max_y):
            tests = [(self.x, self.y - index, self.z), (self.x, self.y + index, self.z)]
            for (x, y, z) in tests:
                if self.min_y <= y <= self.max_y:
                    if (x, y, z) not in self.c:
                        self.i.add((x, y, z))

        # z
        for index in range(self.max_z):
            tests = [(self.x, self.y, self.z - index), (self.x, self.y, self.z + index)]
            for (x, y, z) in tests:
                if self.min_z <= z <= self.max_z:
                    if (x, y, z) not in self.c:
                        self.i.add((x, y, z))

    def can_escape(self, cube: Tuple[int, int, int]) -> bool:
        q = [cube]
        visited = {cube}
        while q:
            (x, y, z) = q.pop()
            # if any of the positions have reached the bounding area then we are good to go
            if (
                x in (self.min_x, self.max_x)
                or y in (self.min_y, self.max_y)
                or z in (self.min_z, self.max_z)
            ):
                return True

            for pos in [
                (x - 1, y, z),
                (x + 1, y, z),
                (x, y - 1, z),
                (x, y + 1, z),
                (x, y, z - 1),
                (x, y, z + 1),
            ]:
                if pos not in visited and pos not in self.c:
                    visited.add(pos)
                    q.append(pos)

        return False

    def __repr__(self) -> str:
        return f"Cube({self.x}, {self.y}, {self.z})"


def run() -> None:

    path = Path(__file__).parent / "data" / "day_18.txt"
    cubes = []

    for line in lines(path):
        (x, y, z) = [int(i) for i in line.split(",")]
        cubes.append(Cube(x, y, z))

    for cube in cubes:
        cube.setup(cubes)

    p1 = sum(cube.num_faces() for cube in cubes)
    assert p1 == 3526

    #  get new cubes
    results: defaultdict[Tuple[int, int, int], int] = defaultdict(int)
    count = 0
    for cube in cubes:
        for cube_pos in cube.is_internal():
            if cube.can_escape(cube_pos) is False:
                count += 1
    assert p1 - count == 2090


if __name__ == "__main__":
    run()
