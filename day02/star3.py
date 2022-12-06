
from __future__ import annotations

import argparse
from enum import Enum
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors
# X means you need to lose, Y means you need to end the round in a draw, and
# Z means you need to win.

class Action(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


winners = {
    Action.Rock: [Action.Scissors],
    Action.Paper: [Action.Rock],
    Action.Scissors: [Action.Paper]

}
DECODE = {
    "A": Action.Rock,
    "B": Action.Paper,
    "C": Action.Scissors,
    "X": Action.Rock,
    "Y": Action.Paper,
    "Z": Action.Scissors
}


def result(opponent, you) -> int:
    if opponent == you:
        return 3  # draw
    if opponent in winners[you]:
        return 6
    return 0


def decode(letter) -> Action:
    return DECODE[letter]


YOU_MOVE = {
    "A": {
        "X": "Z",
        "Y": "X",
        "Z": "Y"
    },
    "B": {
        "X": "X",
        "Y": "Y",
        "Z": "Z"
    },
    "C": {
        "X": "Y",
        "Y": "Z",
        "Z": "X"
    }
}


def compute(s: str) -> int:

    lines = s.splitlines()
    points = 0
    for line in lines:
        print(line[0]+"x"+line[2])
        move = YOU_MOVE[line[0]][line[2]]
        opponent = decode(line[0])
        you = decode(move)
        print(result(opponent, you)+you.value)
        points += result(opponent, you)+you.value
    return points


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
