
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

N = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]


def compute(s: str) -> int:
    lines = s.splitlines()
    cubes = []

    neighbours = []
    for line in lines:
        x, y, z = line.split(",")
        cubes.append((int(x), int(y), int(z)))

    for i in range(0, len(cubes)):
        cube = cubes[i]
        neighbours.append(0)
        for n in N:
            c = tuple([n[a] + cube[a] for a in range(0, 3)])
            if c in cubes:
                neighbours[i] += 1
    free = sum([6-x for x in neighbours])
    return free


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 64


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
