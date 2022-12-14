from __future__ import annotations
from dataclasses import dataclass
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

import helpers


def parse_data() -> Dict[str, Tuple[int, List[str]]]:
    info: Dict[str, Tuple[int, List[str]]] = dict()
    current_dir: List[str] = []
    lines = helpers.lines(Path(__file__).parent / "data" / "day_07.txt")
    for line in lines:
        cmds = line.split()
        if cmds[0] == "$":
            if cmds[1] == "cd":
                arg2 = cmds[2]
                if arg2 == "..":
                    current_dir.pop()
                else:
                    current_dir.append(arg2)
        else:
            dir_path = "/".join(current_dir)
            if dir_path not in info:
                info[dir_path] = (0, [])

            if cmds[0] == "dir":
                info[dir_path][1].append(dir_path + "/" + cmds[1])

            else:
                val, paths = info[dir_path]
                val += int(cmds[0])
                info[dir_path] = (val, paths)
    return info


def get_directory_values(info: Dict[str, Tuple[int, List[str]]]) -> Dict[str, int]:
    return {k: get_nested_count(k, info) for k in info.keys()}


def get_nested_count(key: str, data: Dict[str, Tuple[int, List[str]]]) -> int:
    total = 0
    q = [key]
    while q:
        key = q.pop()
        total += data[key][0]
        for item in data[key][1]:
            q.append(item)
    return total


def part01(dir_values: Dict[str, int]) -> int:
    return sum(v for v in dir_values.values() if v <= 100_000)


def run() -> None:
    info = parse_data()
    dir_values = get_directory_values(info)
    assert part01(dir_values) == 1517599
    assert part02(dir_values) == 2481982


def part02(dir_values: Dict[str, int]) -> int:
    result = 0
    smallest_change = sys.maxsize
    max_size = 70_000_000
    unused = 30_000_000

    free_space = max_size - max(dir_values.values())
    for x in dir_values.values():
        r = free_space + x
        if r >= unused:
            if r < smallest_change:
                smallest_change = r
                result = x
    return result


if __name__ == "__main__":
    run()
