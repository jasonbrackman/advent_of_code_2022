from pathlib import Path


import helpers


def run() -> None:
    lines = helpers.lines(Path(__file__).parent / "data" / "day_04.txt")
    p1 = 0
    p2 = 0
    for line in lines:
        l1, l2, r1, r2 = line.replace("-", ",").split(",")
        lhs = set(range(int(l1), int(l2) + 1))
        rhs = set(range(int(r1), int(r2) + 1))
        if min(lhs) in rhs and max(lhs) in rhs or min(rhs) in lhs and max(rhs) in lhs:
            p1 += 1
        if min(lhs) in rhs or max(lhs) in rhs or min(rhs) in lhs or max(rhs) in lhs:
            p2 += 1

    assert p1 == 644
    assert p2 == 926


if __name__ == "__main__":
    run()
