import time
from pathlib import Path
from typing import List, Dict
import helpers


class CPU:
    CRT_WIDTH = 40
    CRT_ROWS = 6

    def __init__(self) -> None:
        # Registers
        self.r: Dict[str, int] = {
            "x": 1,  # default value starts at 1
        }

        self.clock = 0
        self.stack: List[List[str]] = []

        # For part02
        self.sum = 0

        # For part01
        self.pixel = 0
        self.crt_row = 0
        self.crt = [[" "] * CPU.CRT_WIDTH for _ in range(CPU.CRT_ROWS)]

    def cycle(self) -> None:
        self.clock += 1
        self.pixel = self.clock

        # For part01
        if (self.pixel - 20) % CPU.CRT_WIDTH == 0:  # 20, 60, 100, 140, 180, 220, ...
            self.sum += self.r["x"] * self.pixel

        # for Part02
        if self.pixel % CPU.CRT_WIDTH == 0:
            self.crt_row = (self.crt_row + 1) % CPU.CRT_ROWS

        crt_col = self.pixel % CPU.CRT_WIDTH
        self.crt[self.crt_row][crt_col] = (
            "#" if crt_col in (self.r["x"], self.r["x"] + 1, self.r["x"] + 2) else " "
        )

    def run_program(self) -> None:
        for cmds in self.stack:
            cmd = cmds[0]
            if cmd == "addx":
                """Increase register 'x' by value passed in.  Takes two cycles."""
                self.cycle()
                self.cycle()
                self.r["x"] += int(cmds[1])

            elif cmd == "noop":
                """Takes a single cycle to complete."""
                self.cycle()


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_10.txt")

    cpu = CPU()
    cpu.stack = [line.split() for line in lines]
    cpu.run_program()

    assert cpu.sum == 14860
    assert cpu.crt == [  # RGCEHURK
        list(" ###   ##  #### #### #  # #  # ###  #  #"),
        list("##  # #  #    # #    #  # #  # #  # # # "),
        list("##  # #      #  ###  #### #  # #  # ##  "),
        list(" ###  # ##  #   #    #  # #  # ###  # # "),
        list("## #  #  # #    #    #  # #  # # #  # # "),
        list("##  #  ### #### #### #  #  ##  #  # #  #"),
    ]


if __name__ == "__main__":
    run()
