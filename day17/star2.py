
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP = []
BRICKS = []


class Brick:

    pattern = []
    xmin = 0
    xmax = 0

    def __init__(self, pattern):
        self.pattern = pattern
        self.xmax = max([x[0] for x in pattern])

    def move(self, xs, ys, move):
        pos = [(xs+x, ys+y) for (x, y) in self.pattern]
        for (x, y) in pos:
            if move == ">" and x+1 >= 7:
                return False
            if move == "<" and x-1 <= -1:
                return False
            if y < len(MAP):
                if move == ">":
                    if MAP[y][x+1] != " ":
                        return False
                if move == "<":
                    if MAP[y][x-1] != " ":
                        return False
        return True

    def down(self, xs, ys):
        pos = [(xs+x, ys+y) for (x, y) in self.pattern]
        for (x, y) in pos:
            # print(f"{x},{y} {len(MAP)}")
            if y <= len(MAP):
                if MAP[y-1][x] != " ":
                    return False
        return True

    def addToMap(self, xs, ys):
        pos = [(xs+x, ys+y) for (x, y) in self.pattern]
        for (x, y) in pos:
            if y >= len(MAP):
                MAP.append("       ")
            row = list(MAP[y])
            row[x] = "X"
            MAP[y] = "".join(row)


def printMAP():
    for y in range(len(MAP)-1, -1, -1):
        print("|"+MAP[y]+"|")


def create_thumb():
    odp = []
    for x in range(0, 7):
        for a in range(0, len(MAP)):
            if MAP[len(MAP)-a-1][x] != " ":
                odp.append(a)
                break
    return tuple(odp)


CACHE = {}
CACHE_IDX = []
# STEPS =   2022
STEPS = 1000000000000


def compute(s: str) -> int:
    # __init__
    s = s.strip()
    BRICKS.append(Brick([(0, 0), (1, 0), (2, 0), (3, 0)]))
    BRICKS.append(Brick([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]))
    BRICKS.append(Brick([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]))
    BRICKS.append(Brick([(0, 0), (0, 1), (0, 2), (0, 3)]))
    BRICKS.append(Brick([(0, 0), (0, 1), (1, 0), (1, 1)]))
    MAP.append("=======")
    # TODO: implement solution here!
    step = 0
    brick = 0
    old_step = 0
    old_height = 0
    new_height = 0
    while brick < STEPS:
        thumb = create_thumb()
        key = (thumb, step % len(s), brick % len(BRICKS))
        old_step = step
        old_height = len(MAP)
        if key in CACHE:
            print("Found in CACHE")
            start_cache = CACHE[key][3]
            end_cache = len(CACHE_IDX)-1
            print(f"Start cache from brick nr {start_cache} to {end_cache}")
            suma = 0
            jump = 0
            for a in range(start_cache, end_cache+1):
                suma += CACHE_IDX[a]
            jump = end_cache-start_cache+1
            a = start_cache
            while brick <= STEPS:
                while STEPS-brick > jump:
                    brick = brick+jump
                    new_height = new_height+suma
                new_height = new_height+CACHE_IDX[a]
                print(f"{a} {new_height+len(MAP)-1} {brick}")
                a += 1
                brick += 1

                # key = (thumb, step, brick_idx)
                # c = CACHE[key]
                # print(c[3])
                # step = step+c[2]
                # if step >= len(s):
                #     step = step % len(s)
                # new_height = new_height+c[1]
                # brick = brick+1
                # brick_idx = brick_idx + 1
                # if brick_idx >= len(BRICKS):

            return len(MAP)-1+new_height
        else:
            print("Not found in cache")
        x, y = (2, len(MAP)+3)
        b = BRICKS[brick % len(BRICKS)]
        while (True):
            # prawo/lewo
            move = s[step % len(s)]
            step = step+1
            # print(f"b={brick} step={step} move={move}")
            if b.move(x, y, move):
                if move == ">":
                    x = x+1
                elif move == "<":
                    x = x-1
                else:
                    print(f"ERROR: not know move x{move}x")
            # down
            if b.down(x, y):
                y = y-1
            else:
                b.addToMap(x, y)
                # printMAP()
                CACHE[key] = (create_thumb(), len(
                    MAP)-old_height, step-old_step, brick)
                CACHE_IDX.append(len(MAP)-old_height)
                brick = brick+1
                break
    # printMAP()
    return len(MAP)-1+new_height


INPUT_S = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
# EXPECTED = 3068
EXPECTED = 1514285714288


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
