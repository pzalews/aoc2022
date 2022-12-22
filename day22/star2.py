
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
    for x in MAP:
        print("".join(x))


BORDER = []


def wrapx(x, y, h):
    if 0 <= y < BORDER[0]:
        if x >= BORDER[2]:
            x = BORDER[1]-1
            y = BORDER[2]-1 - y
            h = (h + 2) % 4
        elif x < BORDER[0]:
            x = 0
            y = BORDER[2]-1 - y
            h = (h + 2) % 4
    elif BORDER[0] <= y < BORDER[1]:
        if x >= BORDER[1]:
            x = y + BORDER[0]
            y = BORDER[0]-1
            h = (h + 3) % 4
        elif x < BORDER[0]:
            x = y - BORDER[0]
            y = BORDER[1]
            h = (h + 3) % 4
    elif BORDER[1] <= y < BORDER[2]:
        if x >= BORDER[1]:
            x = BORDER[2]-1
            y = BORDER[2]-1 - y
            h = (h + 2) % 4
        elif x < 0:
            x = BORDER[0]
            y = BORDER[2]-1 - y
            h = (h + 2) % 4
    elif BORDER[2] <= y < BORDER[3]:
        if x < 0:
            x = y - BORDER[1]
            y = 0
            h = (h + 3) % 4
        elif x >= BORDER[0]:
            x = y - BORDER[1]
            y = BORDER[2]-1
            h = (h + 3) % 4
    return x, y, h


def wrapy(x, y, h):
    if 0 <= x < BORDER[0]:
        if y < BORDER[1]:
            y = x + BORDER[0]
            x = BORDER[0]
            h = (h + 1) % 4
        elif y >= BORDER[3]:
            y = 0
            x += BORDER[1]
    elif BORDER[0] <= x < BORDER[1]:
        if y < 0:
            y = x + BORDER[1]
            x = 0
            h = (h + 1) % 4
        elif y >= BORDER[2]:
            y = x + BORDER[1]
            x = BORDER[0]-1
            h = (h + 1) % 4
    elif BORDER[1] <= x < BORDER[2]:
        if y < 0:
            x -= BORDER[1]
            y = BORDER[3]-1
        elif y >= BORDER[0]:
            y = x - BORDER[0]
            x = BORDER[1]-1
            h = (h + 1) % 4
    return x, y, h


def move(x, y, h, order):
    for a in range(0, order):
        ox, oy, oh = x, y, h
        if h == 0:
            x += 1
        elif h == 1:
            y += 1
        elif h == 2:
            x += -1
        elif h == 3:
            y += -1
        if h == 0 or h == 2:
            x, y, h = wrapx(x, y, h)
        else:
            x, y, h = wrapy(x, y, h)

        if MAP[y][x] == "#":
            x, y, h = ox, oy, oh
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
    BORDER.extend(
        tuple(map(int, [len(MAP)/4, len(MAP)/2, 3*len(MAP)/4, len(MAP)])))

    print(BORDER)
    firstx = MAP[0].index(".")
    x, y, h = (firstx, 0, 0)
    for a in range(0, len(steps)):
        m = int(steps[a])
        # print((x, y, h, m))
        x, y, h = move(x, y, h, m)
        if a < len(directions):
            d = directions[a]
            if d == 'R':
                h = (h+1) % 4
            elif d == 'L':
                h = (h + 3) % 4
        # print_map()

    # print_map()
    print((x, y, h))
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
EXPECTED = 5031


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
