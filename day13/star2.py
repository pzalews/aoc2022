
from __future__ import annotations

import argparse
from functools import cmp_to_key
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def mysplit(s):
    odp = []
    if s[0] == "[":
        s = s[1:-1]
    count = 0
    part = []
    for a in s.split(","):
        if a.isnumeric() and count == 0:
            odp.append(a)
            continue
        for b in range(0, len(a)):
            if a[b] == "[":
                count += 1
            if a[b] == "]":
                count -= 1
        part.append(a)
        if count == 0:
            odp.append(",".join(part))
            part = []
    return odp


def compare(a, b):
    a = mysplit(a)
    b = mysplit(b)
    a_size = len(a)
    b_size = len(b)
    size = min(a_size, b_size)
    for x in range(0, size):
        if a[x].isnumeric() and b[x].isnumeric():
            if int(a[x]) < int(b[x]):
                return 1
            elif int(a[x]) > int(b[x]):
                return -1
            continue
        if a[x] != "" and b[x] == "":
            return -1
        if a[x] == "" and b[x] != "":
            return 1
        if a[x] == "" and b[x] == "":
            continue
        if a[x][0] == "[" or b[x][0] == "[":
            if a[x].isnumeric():
                a[x] = "["+a[x]+"]"
            if b[x].isnumeric():
                b[x] = "["+b[x]+"]"
            w = compare(a[x], b[x])
            if w > 0:
                return 1
            if w < 0:
                return -1
    if a_size > size:
        return -1
    if b_size > size:
        return 1
    return 0


def compute(s: str) -> int:
    lines = s.splitlines()
    odp = 0
    add1 = "[[2]]"
    add2 = "[[6]]"
    base = []
    for line in lines:
        if len(line) > 0:
            base.append(line)
    base.append(add1)
    base.append(add2)

    base.sort(key=cmp_to_key(compare), reverse=True)
    x1 = base.index(add1)
    x2 = base.index(add2)

    return (x1+1)*(x2+1)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


def test_single():
    assert compare("[1,1,3,1,1]", "[1,1,5,1,1]") > 0
    assert compare("[[1],[2,3,4]]", "[[1],4]") > 0
    assert compare("[9]", "[[8,7,6]]") < 0
    assert compare("[[4,4],4,4]", "[[4,4],4,4,4]") > 0
    assert compare("[7,7,7,7]", "[7,7,7]") < 0
    assert compare("[]", "[3]") > 0
    assert compare("[[[]]]", "[[]]") < 0
    assert compare("[1,[2,[3,[4,[5,6,7]]]],8,9]",
                   "[1,[2,[3,[4,[5,6,0]]]],8,9]") < 0


def test_mysplit2():
    assert mysplit("[1,[2,[3,[4,[5,6,7]]]],8,9]") == [
        "1", "[2,[3,[4,[5,6,7]]]]", "8", "9"]


def test_problem():
    assert compare("[1,[2,[3,[4,[5,6,7]]]],8,9]",
                   "[1,[2,[3,[4,[5,6,0]]]],8,9]") < 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def test_mysplit():
    assert mysplit("1") == ["1"]
    assert mysplit("[1,2]") == ["1", "2"]
    assert mysplit("[1,[2,3],4]") == ["1", "[2,3]", "4"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
