import copy
import operator
import sys
from collections import deque
from pathlib import Path
from typing import List, Dict, Set, Tuple
import helpers


ops = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.floordiv,
    "*": operator.mul,
    "=": operator.eq,
}


def parse() -> Dict[str, List[str]]:
    path = Path(__file__).parent / "data" / "day_21.txt"
    lut: Dict[str, List[str]] = {}
    for line in helpers.lines(path):
        lhs, *rhs = line.split()
        lhs = lhs.strip(":")
        if len(rhs) == 1:
            rhs = [int(r) for r in rhs]
        lut[lhs] = rhs

    return lut


def spin(goal, lut: Dict[str, List[str]]) -> int:
    q = deque([goal])
    while q:
        key = q.popleft()
        rhs = lut[key]
        if len(lut[goal]) == 1:
            return lut[goal][0]

        if len(rhs) == 3:
            l, m, r = rhs
            if len(lut[l]) == 1 and len(lut[r]) == 1:
                lut[key] = [ops[m](lut[l][0], lut[r][0])]
            else:
                if l not in q:
                    q.append(l)
                if r not in q:
                    q.append(r)

            if key not in q:
                q.append(key)


def spin2(goal, lut: Dict[str, List[str]]) -> Tuple[str, int]:
    q = deque([goal])
    while q:
        key = q.popleft()
        rhs = lut[key]

        if len(lut[goal]) == 1 and isinstance(lut[goal][0], bool):
            # print statements reveal that rhs is always the same
            # lhs changes based on input -- so lets just see if its too low, too high, or juuuust right.
            lut_lhs = lut["zhms"][0]
            lut_rhs = lut["qqqz"][0]
            lut_result = 0

            # is it lt, eq, gt
            if lut_lhs < lut_rhs:
                lut_result = -1
            elif lut_lhs > lut_rhs:
                lut_result = 1

            return lut[goal][0], lut_result

        if len(rhs) == 3:
            l, m, r = rhs
            if len(lut[l]) == 1 and len(lut[r]) == 1:
                lut[key] = [ops[m](lut[l][0], lut[r][0])]
            else:
                if l not in q:
                    q.append(l)
                if r not in q:
                    q.append(r)

            if key not in q:
                q.append(key)


def part01() -> int:
    lut = parse()
    return spin("root", lut)


def part02() -> int:
    lut = parse()

    # patch the 'root'
    goal = "root"
    l, m, r = lut[goal]
    m = "="
    lut[goal] = [l, m, r]

    min_ = 0
    max_ = sys.maxsize
    while True:
        x = (max_ - min_) // 2 + min_
        # need a copy of this lut each time
        temp_lut = copy.deepcopy(lut)
        temp_lut["humn"] = [x]
        result, equality = spin2(goal, temp_lut)

        if equality == 1:
            min_ = x
        elif equality == -1:
            max_ = x
        else:
            for index in range(x - 10, x + 10):
                temp_lut = copy.deepcopy(lut)
                temp_lut["humn"] = [index]
                result, equality = spin2(goal, temp_lut)
                if equality == 0:
                    return index
            break


def run() -> None:
    assert part01() == 93813115694560
    assert part02() == 3910938071092


if __name__ == "__main__":
    run()
