
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve(CACHE, key):
    if key in CACHE:
        value = CACHE[key]
        if value.isnumeric():
            return int(value)
        p1, oper, p2 = value.split(" ")
        if oper == "+":
            return solve(CACHE, p1)+solve(CACHE, p2)
        elif oper == "-":
            return solve(CACHE, p1)-solve(CACHE, p2)
        elif oper == "*":
            return solve(CACHE, p1)*solve(CACHE, p2)
        elif oper == "/":
            return solve(CACHE, p1)/solve(CACHE, p2)
    return "ERROR"


def compute(s: str) -> int:
    CACHE = {}
    lines = s.splitlines()
    for line in lines:
        key, value = line.split(":")
        CACHE[key] = value.strip()

    odp = solve(CACHE, "root")
    return int(odp)


INPUT_S = '''\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''
EXPECTED = 152


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
