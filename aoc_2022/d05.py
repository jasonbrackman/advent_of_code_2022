import copy
from pathlib import Path
from typing import Dict, List, Tuple

import helpers

import re

PATTERN = re.compile(r"[0-9]+")


def parse_data() -> Tuple[Dict[int, List[str]], List[List[int]], List[int]]:
    stacks: Dict[int, List[str]] = dict()
    instructions = []

    lines = helpers.lines_no_strip(Path(__file__).parent / "data" / "day_05.txt")
    header = True
    for line in lines:
        if line == "\n":
            header = False
            continue
        if header:
            for index, col in enumerate(line):
                if col.isalpha():
                    if index not in stacks:
                        stacks[index] = []
                    stacks[index].insert(0, col)

        else:
            instructions.append([int(col) - 1 for col in re.findall(PATTERN, line)])

    keys = list(sorted(stacks.keys()))

    return stacks, instructions, keys


def part01(stacks, instructions, keys) -> str:
    for crates, key_from, key_to in instructions:
        for _ in range(crates + 1):
            stacks[keys[key_to]].append(stacks[keys[key_from]].pop())
    return "".join([stacks[k][-1] for k in keys])


def part02(stacks, instructions, keys) -> str:
    for crates, key_from, key_to in instructions:
        to_move = [stacks[keys[key_from]].pop() for _ in range(crates + 1)]
        stacks[keys[key_to]] += reversed(to_move)
    return "".join([stacks[k][-1] for k in keys])


def run() -> None:
    stacks, instructions, keys = parse_data()
    assert part01(copy.deepcopy(stacks), instructions, keys) == "FJSRQCFTN"
    assert part02(copy.deepcopy(stacks), instructions, keys) == "CJVLJQPHS"


if __name__ == "__main__":
    run()
