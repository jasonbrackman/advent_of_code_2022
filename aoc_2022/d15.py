import re
from pathlib import Path
from typing import Set, Dict, Tuple, List

import helpers

PATTERN = re.compile(r"[-\d]+")
from helpers import Pos


def parse_data(lines: List[str]) -> Tuple[List[Pos], Dict[Tuple[int, int], int]]:
    cheapo = dict()
    sensors = []
    beacons = []
    for line in lines:
        nums = [int(i) for i in re.findall(PATTERN, line)]

        sensor = Pos(nums[1], nums[0])
        beacon = Pos(nums[3], nums[2])
        dist = sensor.manhattan_distance(beacon)

        cheapo[(sensor.row, sensor.col)] = dist
        sensors.append(sensor)
        beacons.append(beacon)
    return beacons, cheapo


def run() -> None:
    path = Path(__file__).parent / "data" / "day_15.txt"
    lines = helpers.lines(path)
    beacons, cheapo = parse_data(lines)

    assert part01(beacons, cheapo, 2_000_000) == 4883971

    high = 4_000_000
    needle = high
    for look in range(needle):
        result = get_items(cheapo, look)
        if len(result) > 0:
            print('s:', look, len(result))
            for x in range(min(result), max(result) + 1):
                if x not in result:
                    val = x * high + look
                    print(f"x={x}, y={look} -> {val}")
                    break


def get_items(cheapo: Dict[Tuple[int, int], int], row_search: int) -> Set[int]:
    items = set()
    for (row, col), distance in cheapo.items():
        if row - distance <= row_search <= row + distance:
            r = abs(row - row_search) - distance
            for val in [col + i for i in range(-abs(r), abs(r) + 1)]:
                if 0 <= val <= 4_000_000:
                    items.add(val)
    if len(items) == 4_000_001:
        items.clear()
    return items


def part01(beacons, cheapo, look) -> int:
    items = set()
    for (row, col), v in cheapo.items():
        if row - v <= look <= row + v:
            r = abs(row - look) - v
            for i in range(-abs(r), abs(r) + 1):
                items.add(col + i)
    bad_items = {b.col for b in beacons if b.row == look}
    return len(items - bad_items)


if __name__ == "__main__":
    run()
