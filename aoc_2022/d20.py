from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Iterator
import helpers
from pathlib import Path


def pprint(lut, data, start: int) -> None:
    visited = [lut[start]]
    while True:
        d = data[start].next
        if lut[d] not in visited:
            visited.append(lut[d])
            start = d
        else:
            break
    print(visited)


def encrypt(lut: Dict[int, int], data: Dict[int, Node], times_to_spin=1) -> None:
    """
    To mix the file, move each number forward or backward in the file a number of positions
    equal to the value of the number being moved. The list is circular, so moving a number
    off one end of the list wraps back around to the other end as if the ends were connected.
    :return:
    """
    for _ in range(times_to_spin):
        for val in lut:
            # Modulus to make positive and reduce number of cycles; -1 since we can't include the val
            lut_02 = lut[val] % (len(lut) - 1)
            if lut_02 == 0:
                continue

            o1 = val
            o2 = val
            for _ in range(lut_02):
                o2 = data[o2].next

            # original prev/next (they need to be fused together
            p1 = data[o1].prev
            n1 = data[o1].next

            # Break apart the goal
            # 1. Find out what the old next was.
            n2 = data[o2].next
            # 2. Replace the old previous with o1
            data[n2].prev = o1
            # 3. Ensure the o2 now goes to o1
            data[o2].next = o1
            # 4. Finally -- update the o1 prev / next
            data[o1].next = n2
            data[o1].prev = o2

            # Fuse the original hole created when removing the original place.
            data[p1].next = n1
            data[n1].prev = p1


@dataclass
class Node:
    prev: int
    next: int


def parts(decryption_key: int, times_to_spin: int) -> int:
    path = Path(__file__).parent / "data" / "day_20.txt"
    nums = helpers.ints(path)

    lut = {i: n * decryption_key for i, n in enumerate(nums)}
    start = [r for r in lut if lut[r] == 0][0]

    bb_start, *bb, bb_end = list(lut.keys())
    aa = [bb_end] + [bb_start] + bb
    cc = bb + [bb_end] + [bb_start]
    data = {i: Node(a, c) for i, (a, c) in enumerate(zip(aa, cc))}

    encrypt(lut, data, times_to_spin)

    all_: List[int] = []
    # iterate through the first three 1000ths places.
    for _ in range(3):
        for index in range(1000):
            start = data[start].next
        all_.append(lut[start])
    # print(all_, len(data))
    return sum(all_)


def run() -> None:
    p1 = parts(1, 1)
    assert p1 == 3 or p1 == 7228

    decryption_key = 811589153
    times_to_spin = 10
    p2 = parts(decryption_key, times_to_spin)
    assert p2 == 4526232706281


if __name__ == "__main__":
    run()
