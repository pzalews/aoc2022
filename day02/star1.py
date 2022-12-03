
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


#A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors

RESULTS={
    "A":{
        "X" : 3,
        "Y" : 6,
        "Z" : 0
    },
    "B": {
        "X" : 0,
        "Y" : 3,
        "Z" : 6
    },
    "C" : {
        "X" : 6,
        "Y" : 0,
        "Z" : 3
    }
}

ADDITIONAL_POINTS = {
    "X" : 1,
    "Y" : 2,
    "Z" : 3
}

def compute(s: str) -> int:

    lines = s.splitlines()
    points = 0
    for line in lines:
        print(line)
        print(line[0]+"x"+line[2])
        print(RESULTS[line[0]][line[2]]+ADDITIONAL_POINTS[line[2]])
        points+=RESULTS[line[0]][line[2]]+ADDITIONAL_POINTS[line[2]]
    return points


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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

