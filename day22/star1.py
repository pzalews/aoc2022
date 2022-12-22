
from __future__ import annotations

import argparse
import os.path

import pytest
import re
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP = []
ORDERS = ""


def print_map():
    for l in MAP:
        print("".join(l))


def wrap(x, y, h):
    while x >= len(MAP[y]) or MAP[y][x] == " ":
        if h == 0:
            x += 1
            if x >= len(MAP[y]):
                x = 0
        elif h == 1:
            y += 1
            if y >= len(MAP):
                y = 0
        elif h == 2:
            x += -1
            if x < 0:
                x = len(MAP[y])-1
        elif h == 3:
            y += -1
            if y < 0:
                y = len(MAP)-1
    return (x, y, h)


def move(x, y, h, order):
    x, y, h = wrap(x, y, h)
    for a in range(0, order):
        ox, oy = x, y
        if h == 0:
            x += 1
            if x >= len(MAP[y]):
                x = 0
        elif h == 1:
            y += 1
            if y >= len(MAP):
                y = 0
        elif h == 2:
            x += -1
            if x < 0:
                x = len(MAP[y])-1
        elif h == 3:
            y += -1
            if y < 0:
                y = len(MAP)-1
        x, y, h = wrap(x, y, h)
        if MAP[y][x] == "#":
            x, y = ox, oy
        MAP[y][x] = str(a % 10)
    return x, y, h


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        if len(line) == 0:
            continue
        MAP.append(list(line))
    ORDERS = "".join(MAP.pop())
    steps = re.split("[RL]", ORDERS)
    directions = re.split("[1234567890]", ORDERS)
    while "" in directions:
        directions.remove("")

    print(len(steps))
    print(len(directions))
    x, y, h = (0, 0, 0)
    for a in range(0, len(steps)):
        m = int(steps[a])
        print((x, y, h, m))
        x, y, h = move(x, y, h, m)
        if a < len(directions):
            d = directions[a]
            if d == 'R':
                h += 1
                if h >= 4:
                    h = 0
            elif d == 'L':
                h += -1
                if h < 0:
                    h = 3
        print_map()

    # print_map()
    return 1000*(y+1)+4*(x+1)+h


INPUT_S = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''
EXPECTED = 6032


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
