from collections import deque
from pathlib import Path
from typing import List, Tuple, Optional, Iterator

import helpers
from helpers import Node

ORD_Z = ord("z")
ORD_E = ord("E")
ORD_S = ord("S")


def is_good_value(old_val: int, new_val: int) -> bool:
    if old_val == ORD_S:
        return True

    new_val = ORD_Z if new_val == ORD_E else new_val
    return new_val <= old_val + 1


def neighbours(row: int, col: int, grid: List[List[str]]) -> Iterator[Tuple[int, int]]:
    old_val = ord(grid[row][col])
    old_val = ORD_Z if old_val == ORD_E else old_val

    # __ Y values
    if row + 1 < len(grid) and is_good_value(old_val, ord(grid[row + 1][col])):
        yield row + 1, col

    if row - 1 >= 0 and is_good_value(old_val, ord(grid[row - 1][col])):
        yield row - 1, col

    # __ X values
    if col + 1 < len(grid[0]) and is_good_value(old_val, ord(grid[row][col + 1])):
        yield row, col + 1

    if col - 1 >= 0 and is_good_value(old_val, ord(grid[row][col - 1])):
        yield row, col - 1


def bfs(row: int, col: int, grid: List[List[str]]) -> Optional[Node[Tuple[int, int]]]:
    q: deque[Node[Tuple[int, int]]] = deque()
    q.append(Node((row, col), None, depth=0))
    visited = {
        (row, col),
    }
    while q:
        node = q.popleft()
        row, col = node.state
        if grid[row][col] == "E":
            return node

        for row, col in neighbours(row, col, grid):
            if (row, col) not in visited:
                visited.add((row, col))
                q.append(Node((row, col), node, depth=node.depth + 1))

    return None


def part01(grid: List[List[str]]) -> Optional[int]:
    row_, col_ = -1, -1
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "S":
                row_, col_ = row, col
                break

    node = bfs(row_, col_, grid)
    if node:
        return node.depth
    return None


def part02(grid: List[List[str]]) -> Optional[int]:
    starts = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "a":
                starts.append((row, col))

    counts = []
    for r, c in starts:
        node = bfs(r, c, grid)
        if node:
            counts.append(node.depth)
    if counts:
        return min(counts)

    return None


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_12.txt")
    grid = [list(line) for line in lines]

    assert part01(grid) == 468
    assert part02(grid) == 459


if __name__ == "__main__":
    run()
