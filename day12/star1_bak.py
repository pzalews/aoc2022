
from __future__ import annotations

import argparse
import os.path

import pytest

import support
import sys
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# BAD SOLUTION - not working for bigger set of data

mapa = []
wins = []

minimum = sys.maxsize*2


def step(xs, ys, xe, ye, path):
    global minimum
    if len(path) > minimum:
        return
    hs = mapa[ys][xs]
    path.append((xs, ys))
    if xs == xe and ys == ye:
        wins.append(path)
        if len(path) < minimum:
            minimum = len(path)
        return
    # LEFT
    if xs > 0 and mapa[ys][xs-1] <= hs+1 and (xs-1, ys) not in path:
        step(xs-1, ys, xe, ye, path.copy())
    # RIGHT
    if xs < len(mapa[0])-1 and mapa[ys][xs+1] <= hs+1 and (xs+1, ys) not in path:
        step(xs+1, ys, xe, ye, path.copy())
    # UP
    if ys > 0 and mapa[ys-1][xs] <= hs+1 and (xs, ys-1) not in path:
        step(xs, ys-1, xe, ye, path.copy())
    # DOWN
    if ys < len(mapa)-1 and mapa[ys+1][xs] <= hs+1 and (xs, ys+1) not in path:
        step(xs, ys+1, xe, ye, path.copy())


def compute(s: str) -> int:
    lines = s.splitlines()
    xs, ys = 0, 0
    xe, ye = 0, 0
    for line in lines:
        # S = -14 ==> E= -28
        points = [ord(x)-ord('a') for x in line]
        mapa.append(points)
    for y in range(0, len(mapa)):
        for x in range(0, len(mapa[0])):
            if mapa[y][x] == -14:
                xs = x
                ys = y
                mapa[y][x] = 0
            if mapa[y][x] == -28:
                xe = x
                ye = y
                mapa[y][x] = 25
    step(xs, ys, xe, ye, [])
    odp = [len(x) for x in wins]
    for p in wins:
        if len(p) == min(odp):
            print(p)

    return min(odp)-1


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
