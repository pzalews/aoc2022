
from __future__ import annotations
from math import lcm
from heapq import heappop, heappush

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move(wh, WALL):
    global Xmax, Ymax, end
    nwh = []
    for x, y, c in wh:
        if c == "^":
            y = y-1
        elif c == "v":
            y = y+1
        elif c == ">":
            x = x+1
        elif c == "<":
            x = x-1
        if (x, y) in WALL:
            if c == "^":
                y = Ymax-2
            elif c == "v":
                y = 1
            elif c == ">":
                x = 1
            elif c == "<":
                x = Xmax-2
        nwh.append((x, y, c))
    return tuple(nwh)


Xmax = 0
Ymax = 0
end = (0, 0)


def load(s):
    lines = s.splitlines()
    WALL = []
    WH = []
    Xmax = len(lines[0])
    Ymax = len(lines)
    start = (0, 0)
    end = (0, 0)

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                WALL.append((x, y))
            elif c in "<>^v":
                WH.append((x, y, c))
            elif y == 0 and c == ".":
                start = (x, y)
            elif y == Ymax-1 and c == ".":
                end = (x, y)
    return WH, WALL, Xmax, Ymax, start, end


def check_wh(wh, x, y):
    for c in "<>^v":
        if (x, y, c) in wh:
            return False
    return True


def compute(s: str) -> int:
    global Xmax, Ymax, end

    WH, WALL, Xmax, Ymax, start, end = load(s)
    period = lcm(Xmax-2, Ymax-2)
    Q = []
    time = 0
    heappush(Q, (time, start))
    CACHE = {}
    SEEN = set()
    CACHE[0] = WH
    for a in range(1, period):
        wh = CACHE[a-1]
        wh = move(wh, WALL)
        CACHE[a] = (wh)

    while Q:
        (time, start) = heappop(Q)
        # print(f"{start},{time}")
        wh = CACHE[(time+1) % period]
        x, y = start
        if start == end:
            return time
        if (time % period, start) in SEEN:
            continue
        SEEN.add((time % period, start))
        if check_wh(wh, x, y):
            heappush(Q, (time+1, (x, y)))
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            npos = (x+dx, y+dy)
            if check_wh(wh, npos[0], npos[1]) and npos not in WALL and Xmax > npos[0] >= 0 and Ymax > npos[1] >= 0:
                heappush(Q, (time+1, npos))

    return 0


INPUT_S = '''\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
'''


EXPECTED = 18


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
