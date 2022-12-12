
from __future__ import annotations

import argparse
import os.path

import pytest

import support
import sys
INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


grid = []
shortest_map = []
wins = []

maxint = sys.maxsize*2
sys.setrecursionlimit(15000)


def step(xs, ys):
    hs = grid[ys][xs]
    steps = shortest_map[ys][xs]
    # LEFT
    if xs > 0 and grid[ys][xs-1] >= hs-1 and \
            shortest_map[ys][xs-1] > steps+1:
        shortest_map[ys][xs-1] = steps+1
        step(xs-1, ys)
    # RIGHT
    if xs < len(grid[0])-1 and grid[ys][xs+1] >= hs-1 and \
            shortest_map[ys][xs+1] > steps+1:
        shortest_map[ys][xs+1] = steps+1
        step(xs+1, ys)
    # UP
    if ys > 0 and grid[ys-1][xs] >= hs-1 and \
       shortest_map[ys-1][xs] > steps+1:
        shortest_map[ys-1][xs] = steps+1
        step(xs, ys-1)
    # DOWN
    if ys < len(grid)-1 and grid[ys+1][xs] >= hs-1 and \
       shortest_map[ys+1][xs] > steps+1:
        shortest_map[ys+1][xs] = steps+1
        step(xs, ys+1)


def compute(s: str) -> int:
    lines = s.splitlines()
    xe, ye = 0, 0
    for line in lines:
        # S = -14 ==> E= -28
        points = [ord(x)-ord('a') for x in line]
        points2 = [maxint for _ in line]
        grid.append(points)
        shortest_map.append(points2)
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] == -14:
                grid[y][x] = 0
            if grid[y][x] == -28:
                xe = x
                ye = y
                grid[y][x] = 25

    shortest_map[ye][xe] = 0

    step(xe, ye)
    min = maxint
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] == 0:
                if shortest_map[y][x] < min:
                    min = shortest_map[y][x]
    return min


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
