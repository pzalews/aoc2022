
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    count = 0
    for line in lines:
    # TODO: implement solution here!
        a1,a2=line.split(",")
        a1s,a1e=a1.split("-")
        a2s,a2e=a2.split("-")
        if int(a1s)<=int(a2s) and int(a1e)>=int(a2e):
            count+=1 
        elif int(a2s)<=int(a1s) and int(a2e)>=int(a1e):
            count+=1 

        #print(f"{a1s}<{a2s} and {a1e}<{a2e}: {count}")
        
    return count


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 2


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

