from __future__ import annotations
import heapq

import helpers
from pathlib import Path
from typing import List, Tuple, Set, Dict, Iterator, Optional

Point = Tuple[int, int]


class Node:
    def __init__(self, state: Point, parent: Optional[Node], depth: int) -> None:
        self.state = state
        self.parent = parent
        self.depth = depth

    def __lt__(self, other) -> bool:
        return bool(self.depth < other.depth)


def parse(path: Path) -> Tuple[List[List[str]], Point, Point, Dict[str, Set[Point]]]:
    rows: List[List[str]] = []
    current: Point = (-1, -1)
    goal: Point = (-1, -1)
    blizzards: Dict[str, Set[Point]] = {
        ">": set(),
        "<": set(),
        "v": set(),
        "^": set(),
    }

    lines = helpers.lines(path)
    for line in lines:
        rows.append(list(line))

    for row in range(len(rows)):
        for col in range(len(rows[0])):
            icon = rows[row][col]
            if icon in ".":
                if row == 0:
                    current = (row, col)
                elif row == len(rows) - 1:
                    goal = (row, col)
            elif icon in ">v<^":
                blizzards[icon].add((row, col))
                rows[row][col] = "."

    return rows, current, goal, blizzards


class Board:
    MOVES = {"*": (0, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}

    def __init__(self, rows, blizzards) -> None:
        self.rows: List[List[str]] = rows
        self._cache: Dict[int, Dict[str, Set[Point]]] = {0: blizzards}

    def tick(self, start_time: int, current: Point, goal: Point) -> Optional[Node]:
        q = []
        start = Node(current, None, start_time)
        heapq.heappush(q, start)
        visited = {
            (start.state, start.depth),
        }

        while q:
            node: Node = heapq.heappop(q)
            if node.state == goal:
                return node

            new_time = node.depth + 1
            for pos in self.neighbours(node.state, new_time):
                if (pos, new_time) not in visited:
                    visited.add((pos, new_time))
                    heapq.heappush(q, Node(pos, node, new_time))

        return None

    def neighbours(self, p1: Point, time: int) -> Iterator[Point]:
        self.update_blizzard_positions(time)
        blizzard_values = self._cache[time].values()

        for _, p2 in Board.MOVES.items():
            row = p1[0] + p2[0]
            col = p1[1] + p2[1]

            if (
                0 <= row < len(self.rows)
                and 0 <= col < len(self.rows[0])
                and self.rows[row][col] != "#"
                and all((row, col) not in vals for vals in blizzard_values)
            ):
                yield row, col

    def update_blizzard_positions(self, time: int) -> None:
        if time not in self._cache:
            blizzards = {}
            for arrow, positions in self._cache[time - 1].items():
                row2, col2 = Board.MOVES[arrow]
                new_positions = set()
                for row, col in positions:
                    row = (row + row2) % len(self.rows)
                    col = (col + col2) % len(self.rows[0])
                    while self.rows[row][col] == "#":
                        row = (row + row2) % len(self.rows)
                        col = (col + col2) % len(self.rows[0])
                    new_positions.add((row, col))
                blizzards[arrow] = new_positions
            self._cache[time] = blizzards


def pprint(rows, blizzards, current, goal) -> None:
    for row in range(len(rows)):
        line = ""
        for col in range(len(rows[0])):
            if rows[row][col] == "#":
                line += "#"
            elif (row, col) == goal:
                line += "G"
            elif (row, col) == current:
                line += "*"
            else:
                icon = "."
                keys = [k for k, v in blizzards.items() if (row, col) in v]
                key_len = len(keys)
                if key_len == 1:
                    icon = keys[0]
                elif key_len > 1:
                    icon = str(key_len)
                line += icon
        print(line)


def run() -> None:
    path = Path(__file__).parent / "data" / "day_24.txt"
    rows, current, goal, blizzards = parse(path)

    # P1
    board = Board(rows, blizzards)
    p1 = board.tick(0, current, goal)
    assert p1.depth == 314

    # p2
    p2 = board.tick(p1.depth, goal, current)
    p3 = board.tick(p2.depth, current, goal)
    assert sum([p1.depth, (p2.depth - p1.depth), (p3.depth - p2.depth)]) == 896


if __name__ == "__main__":
    run()
