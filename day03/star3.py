
from __future__ import annotations

import argparse
import os.path

import pytest

import support

from itertools import islice

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def find_common(tab1,tab2,tab3)->str:
    return list(set(tab1).intersection(tab2).intersection(tab3))[0]


def decoding(s : str) ->int:
    if s.islower():
        return ord(s)-96
    else:
        return ord(s)-38

def compute(s: str) -> int:
    lines = iter(s.splitlines())
    misstook=[]
    while True:
      try:
        s, = set(next(lines)) & set(next(lines)) & set(next(lines))
      except StopIteration:
            break
      misstook.append(s)
        
    suma=0
    for item in misstook:
        print(f"{item}={decoding(item)}")
        suma+=decoding(item)
    return suma


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 70


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

