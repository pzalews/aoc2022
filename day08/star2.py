
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def score(array, x, y) -> int:
    height = array[x][y]
    odp1 = 0
    score = 1
    for a in range(x-1, -1, -1):
        if height > array[a][y]:
            odp1 += 1
        else:
            odp1 += 1
            break
    score = score*odp1
    odp2 = 0
    for a in range(x+1, len(array), 1):
        if height > array[a][y]:
            odp2 += 1
        else:
            odp2 += 1
            break
    score = score*odp2
    odp3 = 0

    for a in range(y-1, -1, -1):
        if height > array[x][a]:
            odp3 += 1
        else:
            odp3 += 1
            break
    score = score*odp3
    odp4 = 0
    for a in range(y+1, len(array[0]), 1):
        if height > array[x][a]:
            odp4 += 1
        else:
            odp4 += 1
            break
    score = score*odp4
    return score


def compute(s: str) -> int:
    lines = s.splitlines()
    trees = []
    for line in lines:
        trees.append([int(x) for x in line])

    score_index = 0
    for x in range(1, len(trees)-1):
        for y in range(1, len(trees[0])-1):
            check = score(trees, x, y)
            if check > score_index:
                score_index = check
    return score_index


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
