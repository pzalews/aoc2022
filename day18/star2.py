
from __future__ import annotations

import argparse
import os.path

import pytest

import support
import sys
sys.setrecursionlimit(15000)


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

N = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

Mx = My = Mz = -1000
mx = my = mz = 1000


def check_outside(x, y, z, outside, air):
    if (x, y, z) in outside:
        return True
    outside.append((x, y, z))
    air.remove((x, y, z))
    for n in N:
        c = (n[0]+x, n[1]+y, n[2]+z)
        if c in air:
            check_outside(c[0], c[1], c[2], outside, air)


def compute(s: str) -> int:
    lines = s.splitlines()
    cubes = []
    global Mx, My, Mz
    global mx, my, mz
    air = []
    neighbours = []
    for line in lines:
        x, y, z = map(int, line.split(","))
        Mx = max(Mx, x)
        My = max(My, y)
        Mz = max(Mz, z)
        mx = min(mx, x)
        my = min(my, y)
        mz = min(mz, z)
        cubes.append((int(x), int(y), int(z)))
    print(f"Size of cubes = {len(cubes)}")
    Mx += 1
    My += 1
    Mz += 1
    mx -= 1
    my -= 1
    mz -= 1
    print(f"X={(mx,Mx)} Y={(my,My)} Z={(mz,Mz)}")
    for x in range(mx, Mx+1):
        for y in range(my, My+1):
            for z in range(mz, Mz+1):
                if (x, y, z) not in cubes:
                    air.append((x, y, z))

    outside = []
    print(f"Air size={len(air)} outside size={len(outside)}")
    check_outside(mx, my, mz, outside, air)
    print(f"Air size={len(air)} outside size={len(outside)}")
    for i in range(0, len(outside)):
        cube = outside[i]
        neighbours.append(0)
        for n in N:
            c = tuple([n[a] + cube[a] for a in range(0, 3)])
            if c in outside:
                neighbours[i] += 1
    outside_wall = 2*(Mx-mx+1)*(My-my+1)+2*(Mx-mx+1) * \
        (Mz-mz+1)+2*(My-my+1)*(Mz-mz+1)
    free = sum([6-x for x in neighbours])
    return free - outside_wall


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 58


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
