import re
from pathlib import Path
from typing import Dict, Tuple, List

import helpers
from helpers import Pos

PATTERN = re.compile(r"[-\d]+")


def parse_data(lines: List[str]) -> Tuple[List[Pos], Dict[Tuple[int, int], int]]:
    sensors: Dict[Tuple[int, int], int] = {}
    beacons = []
    for line in lines:
        nums = [int(i) for i in re.findall(PATTERN, line)]

        sensor = Pos(nums[1], nums[0])
        beacon = Pos(nums[3], nums[2])
        dist = sensor.manhattan_distance(beacon)

        sensors[(sensor.row, sensor.col)] = dist
        beacons.append(beacon)
    return beacons, sensors

def run() -> None:
    path = Path(__file__).parent / "data" / "day_15.txt"
    lines = helpers.lines(path)
    beacons, cheapo = parse_data(lines)
    assert part01(beacons, cheapo, 2_000_000) == 4883971

    p2 = part02(cheapo)
    assert p2 == 12691026767556, "Expected 12691026767556, but received" + str(p2)


def part01(beacons, cheapo, row_search: int) -> int:
    items = set()
    for (row, col), distance in cheapo.items():
        if row - distance <= row_search <= row + distance:
            r = abs(row - row_search) - distance
            for i in range(-abs(r), abs(r) + 1):
                items.add(col + i)

    bad_items = {b.col for b in beacons if b.row == row_search}
    return len(items - bad_items)

def _merge_ranges(ranges):

    ranges.sort(key=lambda x: x[0])
    merged = []

    start = ranges[0][0]
    end = ranges[0][1]

    # Loop through the list of ranges, starting from the second range
    for i in range(1, len(ranges)):
        if ranges[i][0] <= end:
            # If the current range overlaps with the previous range, update the end value
            end = max(end, ranges[i][1])

        else:
            # If the current range does not overlap with the previous range,
            # add the previous range to the list of merged ranges and update
            # the start and end values
            merged.append((start, end))
            start = ranges[i][0]
            end = ranges[i][1]

    # Add the last range to the list of merged ranges
    merged.append((start, end))

    # Return the list of merged ranges
    return merged

def _get_ranges(cheapo: Dict[Tuple[int, int], int], row_search: int) -> List[Tuple[int, int]]:
    ranges = []
    for (row, col), distance in cheapo.items():
        if row - distance <= row_search <= row + distance:
            spread = abs(row - row_search) - distance
            ranges.append((col + -abs(spread), col + abs(spread)))
    return ranges

def part02(cheapo) -> int:
    max_value = 4_000_000
    for y_val in range(max_value):
        result = _get_ranges(cheapo, y_val)
        merged = _merge_ranges(result)
        if len(merged) == 2:
            for x_val in range(merged[0][1] + 1, merged[1][0]):
                return x_val * max_value + y_val


if __name__ == "__main__":
    run()
