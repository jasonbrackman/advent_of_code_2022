from pathlib import Path
from itertools import count
from typing import List, Tuple

import helpers


class CPU:
    def __init__(self) -> None:
        self.x = 1  # register
        self.stack: List[Tuple[str, ...]] = []
        self.cycles = count(1)

        # For part02
        self.sum: List[int] = []

        # For part01
        self.pixel = 0
        self.crt_row = 0
        self.crt = [
            ["."] * 40,
            ["."] * 40,
            ["."] * 40,
            ["."] * 40,
            ["."] * 40,
            ["."] * 40,
        ]

    def get_next_cycle(self) -> None:
        self.pixel = next(self.cycles)

        # For part01
        if self.pixel in (20, 60, 100, 140, 180, 220):
            self.sum.append(self.x * self.pixel)

        # for Part02
        if self.pixel % 40 == 0:
            self.crt_row = (self.crt_row + 1) % 6

        index = self.pixel % 40
        self.crt[self.crt_row][index] = (
            "#" if index in (self.x, self.x + 1, self.x + 2) else "."
        )

    def run_program(self) -> None:
        for cmd in self.stack:
            if cmd[0] == "addx":
                """X register is increased by the arg1
                Takes two cycles."""
                for x in range(2):
                    self.get_next_cycle()
                self.x += int(cmd[1])

            elif cmd[0] == "noop":
                """One cycle to complete."""
                self.get_next_cycle()


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_10.txt")
    cpu = CPU()
    for line in lines:
        cpu.stack.append(line.split())
    cpu.run_program()
    assert sum(cpu.sum) == 14860
    assert cpu.crt == [  # RGCEHURK
        list(".###...##..####.####.#..#.#..#.###..#..#"),
        list("##..#.#..#....#.#....#..#.#..#.#..#.#.#."),
        list("##..#.#......#..###..####.#..#.#..#.##.."),
        list(".###..#.##..#...#....#..#.#..#.###..#.#."),
        list("##.#..#..#.#....#....#..#.#..#.#.#..#.#."),
        list("##..#..###.####.####.#..#..##..#..#.#..#"),
    ]


if __name__ == "__main__":
    run()
