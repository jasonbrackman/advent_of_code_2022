import heapq
import re
from ast import literal_eval
from itertools import zip_longest
from pathlib import Path
from typing import List, Optional

PATTERN = re.compile(r"[0-9]+")


def process_group(left: int | List[int], right: int | List[int]) -> Optional[bool]:
    left = left if isinstance(left, list) else [left]
    right = right if isinstance(right, list) else [right]

    if len(left) == 0 and len(right) > 0 and all(isinstance(i, int) for i in right):
        return True

    if all(isinstance(i, int) for i in left) and all(isinstance(i, int) for i in right):
        for a, b in zip(left, right):
            if a != b:
                return a < b

        if len(left) > len(right):
            return False

        if len(left) < len(right):
            return True

        return None

    for new_left, new_right in zip_longest(left, right, fillvalue=[None]):
        if None in left:
            return True
        elif None in right:
            return False
        else:
            result = process_group(new_left, new_right)
            if result is not None:
                return result

    return False


def sort_packets(groups: List[List[str]]) -> int:
    special = ["[[2]]", "[[6]]"]
    packets = [([2], "[[2]]"), ([6], "[[6]]")]

    heapq.heapify(packets)
    for left, right in groups:
        left_values = [int(i) for i in re.findall(PATTERN, left.replace("[]", "[0]"))]
        right_values = [int(i) for i in re.findall(PATTERN, right.replace("[]", "[0]"))]
        heapq.heappush(packets, (left_values, left))
        heapq.heappush(packets, (right_values, right))

    packs = [heapq.heappop(packets) for _ in range(len(packets))]

    values = [index + 1 for index, pack in enumerate(packs) if pack[1] in special]
    return values[0] * values[1]


def run() -> None:
    puzzle_path = Path(__file__).parent / "data" / "day_13.txt"
    with open(puzzle_path, "rt", encoding="utf8") as handle:
        data = handle.read()
        groups = [group.split() for group in data.split("\n\n")]

    part01 = 0
    for index, (left, right) in enumerate(groups):
        if process_group(literal_eval(left), literal_eval(right)):
            part01 += index + 1
    assert part01 == 5675

    assert sort_packets(groups) == 20383


if __name__ == "__main__":
    run()
