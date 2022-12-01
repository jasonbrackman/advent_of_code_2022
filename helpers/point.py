from __future__ import annotations

from math import sqrt


class Pos:
    """Create a 2D position that contains the row and col values."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __add__(self, other: Pos) -> Pos:
        return Pos(self.row + other.row, self.col + other.col)

    def __sub__(self, other: Pos) -> Pos:
        return Pos(self.row - other.row, self.col - other.col)

    def manhattan_distance(self, other: Pos) -> float:
        y: int = abs(self.row - other.row)
        x: int = abs(self.col - other.col)
        return y + x

    def euclidean_distance(self, other: Pos) -> float:
        y: int = self.row - other.row
        x: int = self.col - other.col
        return sqrt((y * y) + (x * x))
