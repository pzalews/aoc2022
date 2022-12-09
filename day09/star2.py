
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def move_knot(head, tail):
    (xh, yh) = head
    (xt, yt) = tail
    if xh == xt:
        if yh-yt > 1:
            yt = yt+1
        elif yh-yt < -1:
            yt = yt-1
        return xt, yt
    elif yh == yt:
        if xh-xt > 1:
            xt += 1
        elif xh-xt < -1:
            xt -= 1
        return xt, yt
    # diagonal move1
    if abs(xh-xt) > 1 or abs(yh-yt) > 1:
        if xh-xt > 0 and yh-yt > 0:
            xt += 1
            yt += 1
        elif xh-xt < 0 and yh-yt > 0:
            xt -= 1
            yt += 1
        elif xh-xt < 0 and yh-yt < 0:
            xt -= 1
            yt -= 1
        elif xh-xt > 0 and yh-yt < 0:
            xt += 1
            yt -= 1
    return (xt, yt)


def compute(s: str) -> int:
    lines = s.splitlines()
    x, y = 0, 0  # HEAD
    knots = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
             (0, 0), (0, 0), (0, 0)]
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
            # move knots
            for a in range(0, len(knots)):
                tail = knots[a]
                head = (x, y)
                if a > 0:
                    head = knots[a-1]
                knots[a] = move_knot(head, tail)
            tail_history.append(knots[len(knots)-1])
    return len(dict.fromkeys(tail_history))


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
