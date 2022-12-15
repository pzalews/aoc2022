
from __future__ import annotations

import argparse
import os.path

import pytest
import sys
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP = []
LINE = 2000000
# LINE = 10

intmaximum = sys.maxsize*2


def distance(x1, y1, x2, y2):
    return abs(x1-x2)+abs(y1-y2)


def is_beacon(x, y):
    for sensor in MAP:
        b = sensor["beacon"]
        if b[0] == x and b[1] == y:
            return True
    return False


def is_in_range(x, y):
    for sensor in MAP:
        s = sensor["sensor"]
        if distance(x, y, s[0], s[1]) <= sensor["range"]:
            return True
    return False


def compute(s: str, testline=LINE) -> int:
    lines = s.splitlines()
    for line in lines:
        _, _, sx, sy, _, _, _, _, bx, by = line.split()
        sx = int(sx.split("=")[1][0:-1])
        sy = int(sy.split("=")[1][0:-1])
        bx = int(bx.split("=")[1][0:-1])
        by = int(by.split("=")[1])
        rangesb = distance(sx, sy, bx, by)
        MAP.append({"beacon": (bx, by), "sensor": (sx, sy), "range": rangesb})
    minx = min([x["sensor"][0]-x["range"] for x in MAP])
    maxx = max([x["sensor"][0]+x["range"] for x in MAP])
    print(minx, maxx)
    count = 0
    for x in range(minx, maxx):
        if is_in_range(x, testline):
            if is_beacon(x, testline):
                continue
            count += 1
    return count


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 26


@ pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
