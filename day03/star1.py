
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def find_common(tab1,tab2)->str:
    return list(set(tab1).intersection(tab2))[0]


def decoding(s : str) ->int:
    if s.islower():
        return ord(s)-96
    else:
        return ord(s)-38

def compute(s: str) -> int:
    lines = s.splitlines()
    racksack=[]
    misstook=[]
    for line in lines:
        compartment1=line[0:int(len(line)/2)]
        compartment2=line[int(len(line)/2):len(line)]
        racksack.append([compartment1,compartment2])
        misstook.append(find_common(compartment1,compartment2))

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
EXPECTED = 157


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

