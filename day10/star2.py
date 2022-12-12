
from __future__ import annotations
from math import floor

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

INPUT_FRQ = [20, 60, 100, 140, 180, 220]

odp = 0
freq = []
crt = []


def display_crt():
    for row in crt:
        print("".join(row))


def decode_xy(clock):
    while clock > 40*9:
        clock = clock-40*9
    x = clock % 40
    y = floor(clock/40)
    return x, y


def draw_pixel(x, y, c):
    if y >= len(crt):
        crt.append([])
    row = crt[y]
    if x >= len(row):
        row.append(c)


def step(clock, x, odp):
    x1, y1 = decode_xy(clock)
    if x1 == x-1 or x1 == x or x1 == x+1:
        draw_pixel(x1, y1, "X")
    else:
        draw_pixel(x1, y1, " ")
    clock += 1
    if clock in INPUT_FRQ:
        freq.append((clock, clock*x))
        odp = odp+clock*x
    return clock, odp


def compute(s: str) -> int:
    odp = 0
    x = 1
    clock = 0
    lines = s.splitlines()
    for line in lines:
        if line[0] == "a":
            _, value = line.split()
            for _ in range(0, 2):
                clock, odp = step(clock, x, odp)
            x += int(value)
        else:
            clock, odp = step(clock, x, odp)
    display_crt()
    return odp


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = 13140


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
