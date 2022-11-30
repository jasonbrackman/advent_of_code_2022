from typing import List


def lines(path: str) -> List[str]:
    with open(path, "r") as text:
        return [line.strip() for line in text.readlines()]


def ints(path: str) -> List[int]:
    with open(path, "r") as text:
        return [int(i) for i in text.readlines()]
