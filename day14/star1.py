
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP = {}


def print_map():
    keys = MAP.keys()
    minx = min([x[0] for x in keys])
    maxx = max([x[0] for x in keys])
    miny = min([x[1] for x in keys])
    maxy = max([x[1] for x in keys])
    for y in range(miny, maxy+1):
        print("")
        for x in range(minx, maxx+1):
            if (x, y) in keys:
                print(MAP[(x, y)], end='')
            else:
                print(" ", end='')


def sand(x, y):
    keys = MAP.keys()
    minx = min([x[0] for x in keys])
    maxx = max([x[0] for x in keys])
    miny = min([x[1] for x in keys])
    maxy = max([x[1] for x in keys])
    for b in range(y, maxy+1):
        if (x, b+1) not in keys:
            continue
        if (x-1, b+1) not in keys:
            x = x-1
            continue
        if (x+1, b+1) not in keys:
            x = x+1
            continue
        if minx <= x <= maxx and miny <= b <= maxy:
            MAP[(x, b)] = "o"
            return True
        else:
            return False
    return False


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        d = line.split(" ")
        oldx, oldy = (-1, -1)
        for a in range(0, len(d), 2):
            x, y = d[a].split(",")
            x, y = (int(x), int(y))
            MAP[(x, y)] = "#"
            if oldx > 0 and oldy > 0:
                for a in range(oldx, x+1):
                    for b in range(oldy, y+1):
                        MAP[(a, b)] = "#"
                    for b in range(oldy, y-1, -1):
                        MAP[(a, b)] = "#"
                for a in range(oldx, x-1, -1):
                    for b in range(oldy, y+1):
                        MAP[(a, b)] = "#"
                    for b in range(oldy, y-1, -1):
                        MAP[(a, b)] = "#"
            oldx = x
            oldy = y
    count = 0
    MAP[(500, 0)] = "O"
    while (True):
        if sand(500, 0):
            count += 1
        else:
            break

    MAP[(500, 0)] = "O"
    return count


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 24


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
