
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    lines = s.splitlines()
    stacks = []
    for line in lines:
        # stacks
        if line[1] != "1":
            containers = [line[x] for x in range(1, len(line), 4)]
            if len(stacks) < len(containers):
                for a in range(0, len(containers)):
                    stacks.append([])
            # inserting containers
            for a in range(0, len(containers)):
                if containers[a] != " ":
                    stacks[a].append(containers[a])
        else:
            break

    # odwrocenie kontenerów
    for a in range(0, len(stacks)):
        stacks[a].reverse()

    # interpretacja
    for line in lines:
        commands = line.split()
        if len(commands) > 1 and commands[0] == "move":
            count = int(commands[1])
            froms = int(commands[3])-1
            to = int(commands[5])-1
            for a in range(0, count):
                stacks[to].append(stacks[froms].pop())
    # wynik
    odp = [stacks[a].pop() for a in range(0, len(stacks))]

    return "".join(odp)


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
