
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move_tail(x, y, xt, yt):
    if x == xt:
        if y-yt > 1:
            yt = yt+1
        elif y-yt < -1:
            yt = yt-1
        return xt, yt
    elif y == yt:
        if x-xt > 1:
            xt += 1
        elif x-xt < -1:
            xt -= 1
        return xt, yt
    # diagonal move1
    if abs(x-xt) > 1 or abs(y-yt) > 1:
        if x-xt > 0 and y-yt > 0:
            xt += 1
            yt += 1
        elif x-xt < 0 and y-yt > 0:
            xt -= 1
            yt += 1
        elif x-xt < 0 and y-yt < 0:
            xt -= 1
            yt -= 1
        elif x-xt > 0 and y-yt < 0:
            xt += 1
            yt -= 1
    return xt, yt


def compute(s: str) -> int:
    lines = s.splitlines()
    x, y = 0, 0
    xt, yt = 0, 0
    tail_history = []
    for line in lines:
        dir, steps = line.split()
        for _ in range(0, int(steps)):
            if dir == "R":
                x = x+1
            elif dir == "L":
                x = x-1
            elif dir == "D":
                y = y-1
            elif dir == "U":
                y = y+1
            else:
                print("BAGGGG")
        # move tail
            xt, yt = move_tail(x, y, xt, yt)
            tail_history.append((xt, yt))
    return len(dict.fromkeys(tail_history))


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
