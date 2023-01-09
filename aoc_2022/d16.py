from __future__ import annotations

import copy
import heapq
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

import helpers


@dataclass
class Valve:
    rate: int
    childs: List[str] = field(default_factory=list)


def parse(path: Path) -> Dict[str, Valve]:
    pattern = re.compile(
        r"Valve (\S+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
    )
    lines = helpers.lines(path)
    valves: Dict[str, Valve] = dict()
    for line in lines:
        valve, rate, childs = re.findall(pattern, line)[0]
        valves[valve] = Valve(int(rate), childs.split(", "))
    return valves


@dataclass(order=True)
class Node:
    state: str
    total: int
    open: Set[str]
    depth: int

    def hash(self) -> str:
        return f'{self.state}, {self.total}, {self.depth}'


@dataclass(order=True)
class N2:
    s1: str
    s2: str
    total: int
    open: Set[str]
    depth: int

    def hash(self) -> str:
        return f'{self.s1}, {self.s2}, {self.total}, {self.depth}'


def bfs(start: str, valves: Dict[str, Valve], timer: int) -> int:
    open_valves = {k for k, v in valves.items() if v.rate == 0}  # Some valves are worth zero; no need to open.

    q: List[Tuple[int, Node]] = []

    node = Node(state=start, total=0, open=open_valves, depth=1)
    heapq.heappush(q, (0, node))

    v: Set[str] = {node.hash(), }

    highest = 0
    count = 0

    while q:
        count += 1
        cost, node = heapq.heappop(q)

        if node.depth == timer:
            if node.total > highest:
                highest = max(node.total, highest)
                # print(f"[{count}] Current High:", highest, node)
        else:
            # Go through all possible updates; even skipping opening the non-open valve
            for child in valves[node.state].childs:
                new_node = Node(
                    state=child,
                    total=node.total,
                    open=set(node.open),
                    depth=node.depth + 1
                )

                if new_node.hash() not in v:
                    v.add(new_node.hash())
                    heapq.heappush(q, (-node.total, new_node))

            # Valve already open; move to next valve...
            if node.state not in node.open:
                node_total = node.total + valves[node.state].rate * (timer - node.depth)
                opens = set(node.open)
                opens.add(node.state)
                nn = Node(state=node.state, total=node_total, open=opens, depth=node.depth + 1)

                if nn.hash() not in v:
                    v.add(nn.hash())
                    heapq.heappush(q, (-nn.total, nn))

    return highest


def bfs2(start: str, valves: Dict[str, Valve], timer: int) -> int:
    open_valves = {k for k, v in valves.items() if v.rate == 0}  # valve AA will be open; no need to open it again.

    q: List[Tuple[int, N2]] = []
    node = N2(s1=start, s2=start, total=0, open=open_valves, depth=1)
    heapq.heappush(q, (0, node))
    highest = 0
    count = 0
    v: Set[str] = {node.hash(), }
    while q:
        count += 1
        cost, node = heapq.heappop(q)

        if node.depth == timer:
            if node.total > highest:
                highest = max(node.total, highest)
                # print(f"[{count}] Current High:", highest, node)
        else:
            # choose to skip and move and on
            for child01 in valves[node.s1].childs:
                for child02 in valves[node.s2].childs:
                    nn = N2(
                        s1=child01,
                        s2=child02,
                        total=node.total,
                        open=set(node.open),
                        depth=node.depth + 1,
                    )

                    if nn.hash() not in v:
                        v.add(nn.hash())
                        heapq.heappush(q, (-node.total, nn))

            # possibly both of the nodes can be opened...
            if node.s1 not in node.open and node.s2 not in node.open:
                opens = set(node.open)
                opens.add(node.s1)
                node_total = node.total + valves[node.s1].rate * (timer - node.depth)
                if node.s1 != node.s2:
                    opens.add(node.s2)
                    node_total += valves[node.s2].rate * (timer - node.depth)

                nn = N2(s1=node.s1, s2=node.s2, total=node_total, open=opens, depth=node.depth + 1)
                if nn.hash() not in v:
                    v.add(nn.hash())
                    heapq.heappush(q, (-nn.total, nn))

            # if s1 not in node.open; open it, then go through the children of s2
            elif node.s1 not in node.open and node.s2 in node.open:
                opens = set(node.open)
                opens.add(node.s1)
                node_total = node.total + valves[node.s1].rate * (timer - node.depth)
                for child02 in valves[node.s2].childs:
                    nn = N2(s1=node.s1, s2=child02, total=node_total, open=opens, depth=node.depth + 1)
                    if nn.hash() not in v:
                        v.add(nn.hash())
                        heapq.heappush(q, (-nn.total, nn))

            elif node.s1 in node.open and node.s2 not in node.open:
                node.open.add(node.s2)
                node_total = node.total + valves[node.s2].rate * (timer - node.depth)
                for child01 in valves[node.s1].childs:
                    nn = N2(
                        s1=child01, s2=node.s2, total=node_total, open=set(node.open), depth=node.depth + 1,
                    )

                    if nn.hash() not in v:
                        v.add(nn.hash())
                        heapq.heappush(q, (-nn.total, nn))

    return highest


def run() -> None:
    path = Path(__file__).parent / "data" / "day_16.txt"
    valves = parse(path)
    p1 = bfs("AA", valves, 30)
    assert p1 in (1651, 1991)

    p2 = bfs2("AA", valves, 26)
    assert p2 in (1707, 2705)


if __name__ == "__main__":
    run()

