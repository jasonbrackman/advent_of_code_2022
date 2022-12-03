from pathlib import Path
import helpers


def run() -> None:
    totals = []
    count = 0
    for line in helpers.lines(Path("./data/day_01.txt")):
        if line == "":
            totals.append(count)
            count = 0
        else:
            count += int(line)

    assert max(totals) == 66306
    assert sum(list(sorted(totals))[-3:]) == 195292


if __name__ == "__main__":
    run()
