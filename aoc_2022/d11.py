import heapq
import math
import operator
import re
from collections import deque, defaultdict
from pathlib import Path
from typing import List, Dict, Deque

PATTERN = re.compile(r"[0-9]+")


class Monkey:
    def __init__(self) -> None:
        self.items: Deque[int] = deque()
        self.operation: List[str] = []
        self.test: List[int] = []
        self.inspected = 0
        self.lcm = 0

    def run_operation(self, item: int) -> int:
        input1, cmd, input2 = self.operation
        arg1 = item if input1 == "old" else int(input1)
        arg2 = item if input2 == "old" else int(input2)
        op = operator.mul if cmd == "*" else operator.add
        return int(op(arg1, arg2)) % self.lcm

    def run_test(self, item: int) -> int:
        val, if_true, if_false = self.test
        return if_true if item % val == 0 else if_false

    def inspect(self, worry_level: int) -> Dict[int, List[int]]:
        results: Dict[int, List[int]] = defaultdict(list)
        while self.items:
            self.inspected += 1
            item = self.items.popleft()
            result = self.run_operation(item)
            to_result = result // worry_level
            to_monkey = self.run_test(to_result)
            results[to_monkey].append(to_result)

        return results

    def load(self, data: List[str]) -> None:
        for index, line in enumerate(data):
            if index == 0:
                continue
            elif index == 1:
                self.items += [int(i) for i in re.findall(PATTERN, line)]
            elif index == 2:
                items = [item for item in line.split()]
                arg1, op, arg2 = items[-3:]
                self.operation = [arg1, op, arg2]
            elif index in (3, 4, 5):
                val = re.findall(PATTERN, line)[-1]
                self.test.append(int(val))

    def __repr__(self) -> str:
        return f"Monkey({self.items}, {self.operation}, {self.test}"


def parse_for_monkeys() -> List[Monkey]:
    with open((Path(__file__).parent / "data" / "day_11.txt"), "r") as handle:
        monkey_data = handle.read().split("\n\n")

    monkeys = []

    for data in monkey_data:
        m = Monkey()
        m.load(data.split("\n"))
        monkeys.append(m)

    lcm = math.lcm(*[m.test[0] for m in monkeys])
    for m in monkeys:
        m.lcm = lcm

    return monkeys


def simian_shenanigans(rounds: int, worry_level: int) -> int:
    monkeys = parse_for_monkeys()
    for _ in range(rounds):
        for monkey in monkeys:
            for k, v in monkey.inspect(worry_level).items():
                monkeys[k].items += v

    a, b = heapq.nlargest(2, [m.inspected for m in monkeys])
    return int(operator.mul(a, b))


def run() -> None:
    assert simian_shenanigans(20, 3) == 110220
    assert simian_shenanigans(10_000, 1) == 19457438264


if __name__ == "__main__":
    run()
