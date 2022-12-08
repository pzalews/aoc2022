
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_visible(array, x, y) -> bool:
    height = array[x][y]
    odp = 0
    # breakpoint()
    for a in range(0, x):
        if height <= array[a][y]:
            odp += 1
            break
    for a in range(x+1, len(array), 1):
        if height <= array[a][y]:
            odp += 1
            break

    for a in range(0, y):
        if height <= array[x][a]:
            odp += 1
            break
    for a in range(y+1, len(array[0]), 1):
        if height <= array[x][a]:
            odp += 1
            break
    # print(f"checking {x}{y} {height} result {odp}")
    if odp == 4:  # jezeli jest niewidoczne z kazdej strony
        return False
    else:
        return True


def compute(s: str) -> int:
    lines = s.splitlines()
    trees = []
    for line in lines:
        trees.append([int(x) for x in line])

    odp = 0
    odp = len(trees)*2+len(trees[0])*2-4  # outside
    for x in range(1, len(trees)-1):
        for y in range(1, len(trees[0])-1):
            if is_visible(trees, x, y):
                odp += 1
    return odp


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
