
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_me(CACHE, key):
    if key in CACHE:
        if key == "humn":
            return True
        value = CACHE[key]
        if value.isnumeric():
            return False
        p1, _, p2 = value.split(" ")
        return is_me(CACHE, p1) or is_me(CACHE, p2)


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
    return "ERROR1"


def reverse_solve(CACHE, key, r_value):
    print(f"reverse_solve on {key} with {r_value}")
    if key in CACHE:
        value = CACHE[key]
        if key == "humn":
            return r_value
        if value.isnumeric() and key != "humn":
            return int(value)
        p1, oper, p2 = value.split(" ")
        know, unknow = (None, None)
        position2 = False
        if is_me(CACHE, p1):
            unknow = p1
            know = p2
        elif is_me(CACHE, p2):
            unknow = p2
            know = p1
            position2 = True
        else:
            print(f"reverse_solve on both know: {p1} and {p2}")
            return "ERROR2"
        if oper == "+":
            return reverse_solve(CACHE, unknow, r_value-solve(CACHE, know))
        elif oper == "-" and not position2:
            return reverse_solve(CACHE, unknow, r_value+solve(CACHE, know))
        elif oper == "-" and position2:
            return reverse_solve(CACHE, unknow, solve(CACHE, know)-r_value)
        elif oper == "/" and not position2:
            return reverse_solve(CACHE, unknow, r_value*solve(CACHE, know))
        elif oper == "/" and position2:
            return reverse_solve(CACHE, unknow, solve(CACHE, know)/r_value)
        elif oper == "*":
            return reverse_solve(CACHE, unknow, r_value/solve(CACHE, know))
        else:
            print("ERROR3")


def compute(s: str) -> int:
    CACHE = {}
    lines = s.splitlines()
    for line in lines:
        key, value = line.split(":")
        CACHE[key] = value.strip()
    root = CACHE["root"]
    r1, _, r2 = root.split(" ")
    r_value = 0
    r_solve = ""
    if is_me(CACHE, r1):
        print("r1")
        r_value = solve(CACHE, r2)
        r_solve = r1
    elif is_me(CACHE, r2):
        print("r2")
        r_value = solve(CACHE, r1)
        r_solve = r2
    else:
        print("ERROR?")

    odp = reverse_solve(CACHE, r_solve, r_value)
    return odp


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
EXPECTED = 301


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
