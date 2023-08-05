from __future__ import annotations

from collections import deque
from typing import Dict, List, Set, Tuple
from pathlib import Path
import helpers


Costs = Dict[int, Set[Tuple[int, int]]]
Blueprints = Dict[int, Costs]
Bank = List[int]
Bots = List[int]


class RNode:
    def __init__(self, bank: Bank, bots: Bots, time: int):
        self.bank = bank
        self.bots = bots
        self.time = time

    def hash(self) -> str:
        return str(self.bank + self.bots) + str(self.time)


def menu(node: RNode, costs: Costs, max_costs: List[int], minutes: int) -> List[int]:
    choices = []
    for bot in range(4):
        if 0 in choices:
            continue
        # check if you have more than can be used for a particular type in the time provided.
        if bot != 0 and node.bank[bot] >= max_costs[bot] * (minutes - node.time):
            continue
        if all(node.bank[part] >= cost for part, cost in costs[bot]):
            choices.append(bot)
    return choices


def search(costs: Costs, bank: Bank, bots: Bots, minutes: int) -> int:
    max_costs = cost_maximums(costs)
    start = RNode(bank, bots, 0)
    q = deque([start])
    v = {
        start.hash(),
    }

    current_time = 0

    result = 0
    while q:
        node = q.popleft()
        if node.time > current_time:
            current_time = node.time
            v.clear()
        if node.time == minutes:  # time must have exceeded
            # if node.bank[0] > result:
            #     print('geode:', node.bank[0], 'at start of time', node.time)
            result = max(result, node.bank[0])
            continue

        # _choices to purchase
        # -- in an effort to recude amount of state; throw away state that is impossible to use.  For
        #    example, the bank can fill up to a point it can never be spent in time left.
        minutes_left = minutes - node.time
        for ii in range(1, 4):
            if node.bank[ii] > max_costs[ii] * minutes_left:
                node.bank[ii] = max_costs[ii] * minutes_left

        frontier = menu(node, costs, max_costs, minutes)

        # _collect
        new_bank = [balance + bot for balance, bot in zip(node.bank, node.bots)]
        for index in frontier:
            new_bots = node.bots[:]
            new_bots[index] += 1
            new_bank2 = new_bank[:]
            for part, cost in costs[index]:
                new_bank2[part] -= cost

            new_node = RNode(new_bank2, new_bots, node.time + 1)
            if new_node.hash() not in v:
                v.add(new_node.hash())
                if index == 0:
                    q.appendleft(new_node)
                else:
                    q.append(new_node)

        # _account for doing nothing
        if 0 not in frontier:
            new_node = RNode(new_bank, node.bots[:], node.time + 1)
            if new_node.hash() not in v:
                v.add(new_node.hash())
                q.append(new_node)

    return result


def cost_maximums(costs: Costs) -> List[int]:
    # geode, obsidian, clay, ore
    max_costs: List[int] = [99_999, 0, 0, 0]
    for _bot, parts in costs.items():
        for part, count in parts:
            max_costs[part] = max(max_costs[part], count)
    return max_costs


def parse_blueprints() -> Blueprints:
    lut: Dict[str, int] = {"geode": 0, "obsidian": 1, "clay": 2, "ore": 3}
    blueprints: Blueprints = {}
    path = Path(__file__).parent / "data" / "day_19.txt"
    for i, line in enumerate(helpers.lines(path), start=1):
        blueprints[i] = {}
        _, data = line.split(":")
        for d in data.split(". "):
            robot_type, items = d.strip().split("costs")
            robot_type = robot_type.split()[1].strip()
            parts_ = [part.split() for part in items.split("and")]
            parts = {(lut[p.strip(".")], int(v)) for (v, p) in parts_}
            blueprints[i][lut[robot_type]] = parts
    return blueprints


def part01() -> int:
    total = 0
    blueprints = parse_blueprints()
    bank = [0, 0, 0, 0]  # geode, obsidian, clay, ore
    bots = [0, 0, 0, 1]
    for bp in blueprints:
        r = search(blueprints[bp], bank, bots, 24)
        total += r * bp
    return total


def part02() -> int:
    total2 = []
    blueprints = parse_blueprints()
    bank = [0, 0, 0, 0]  # geode, obsidian, clay, ore
    bots = [0, 0, 0, 1]
    for bp in blueprints:
        if bp > 3:
            continue
        r = search(blueprints[bp], bank, bots, 32)
        total2.append(r)

    # _Calc result
    result = total2[0]
    for item in total2[1:]:
        result *= item
    return result


def run() -> None:
    p1 = part01()
    p2 = part02()
    assert p1 == 1528
    assert p2 == 16926


if __name__ == "__main__":
    part01()
