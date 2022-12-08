from pathlib import Path
from typing import List

import helpers


def is_visible(row: int, col: int, height: int, grid: List[List[int]]) -> bool:
    return False in (
        any(grid[r][col] >= height for r in range(row)),  # Up
        any(grid[r][col] >= height for r in range(row + 1, len(grid))),  # Down
        any(grid[row][c] >= height for c in range(col)),  # left
        any(grid[row][c] >= height for c in range(col + 1, len(grid[0]))),  # right
    )


def is_visible_count(row: int, col: int, height: int, grid: List[List[int]]) -> int:

    up = 0
    for r in range(row - 1, -1, -1):
        up += 1
        if not grid[r][col] < height:
            break

    left = 0
    for c in range(col - 1, -1, -1):
        left += 1
        if not grid[row][c] < height:
            break

    down = 0
    for r in range(row + 1, len(grid)):
        down += 1
        if not grid[r][col] < height:
            break

    right = 0
    for c in range(col + 1, len(grid[0])):
        right += 1
        if not grid[row][c] < height:
            break

    return up * left * down * right


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_08.txt")
    grid = [[int(c) for c in line] for line in lines]

    scores = []
    totals = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            result = is_visible(r, c, grid[r][c], grid)
            totals.append(result)
            scores.append(is_visible_count(r, c, grid[r][c], grid))

    assert sum(totals) == 1715
    assert max(scores) == 374400


if __name__ == "__main__":
    run()
