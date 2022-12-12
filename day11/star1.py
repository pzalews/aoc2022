from __future__ import annotations

import argparse
import os.path

import pytest

import support
from math import floor

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

monkeys = []


class Monkey:
    items = []
    operation = ""
    test_div = 0
    test_true = 0
    test_false = 0
    inspected_items = 0

    def __init__(self, items, operation,
                 test_div, test_true, test_false) -> None:
        self.items = items
        self.operation = operation
        self.test_div = test_div
        self.test_true = test_true
        self.test_false = test_false

    def __str__(self) -> str:
        return " ".join([str(x) for x in self.items])

    def turn(self):
        copy = self.items
        self.items = []
        for item in copy:
            self.inspected_items += 1
            item = self.do_operation(item)
            item = floor(item/3)
            if item % self.test_div == 0:
                monkeys[self.test_true].add(item)
            else:
                monkeys[self.test_false].add(item)

    def add(self, item):
        self.items.append(item)

    def do_operation(self, item):
        _, _, a1, op, a2 = self.operation.split()
        if a1 == "old":
            a1 = item
        if a2 == "old":
            a2 = item
        a1 = int(a1)
        a2 = int(a2)
        if op == "*":
            return a1 * a2
        elif op == "+":
            return a1+a2
        elif op == "-":
            return a1-a2
        else:
            raise Exception("Unknow operation", op)


def compute(s: str) -> int:
    lines = s.splitlines()
    nr_monkey = 0
    starting_items = []
    operation = ""
    test_numer = 0
    test_true, test_false = 0, 0
    for line in lines:
        if len(line) > 0:
            if line.startswith("Monkey"):
                nr_monkey = line.split()[1]
            else:
                cmd, arg = line.split(":")
                if cmd.endswith("items"):
                    starting_items = [int(x) for x in arg.split(",")]
                elif cmd.endswith("Operation"):
                    operation = arg.strip()
                elif cmd.endswith("Test"):
                    _, _, test_numer = arg.split()
                    test_numer = int(test_numer)
                elif cmd.endswith("true"):
                    _, _, _, test_true = arg.split()
                    test_true = int(test_true)
                elif cmd.endswith("false"):
                    _, _, _, test_false = arg.split()
                    test_false = int(test_false)
        else:
            m = Monkey(starting_items, operation,
                       test_numer, test_true, test_false)
            print(f"{len(monkeys)} == {nr_monkey}")
            monkeys.append(m)
    for _ in range(0, 20):
        for m in monkeys:
            m.turn()
    inspection = [m.inspected_items for m in monkeys]
    inspection.sort(reverse=True)

    return inspection[0]*inspection[1]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1

'''
EXPECTED = 10605


@ pytest.mark.parametrize(
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
