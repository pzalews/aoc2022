
from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

dir = {}


def find_size(key):
    if key not in dir:
        return 0
    size = 0
    # for a in dir[key]:
    #     size += a["size"]
    for a in dir.keys():
        if a.startswith(key):
            for b in dir[a]:
                size += b["size"]
    return size


def compute(s: str) -> int:
    pwd = ""
    lines = s.splitlines()
    for line in lines:
        if line[0] == '$':
            cmds = line.split()
            if cmds[1] == "cd":
                if cmds[2] == "/":
                    pwd = "/"
                elif cmds[2] == "..":
                    pwd = "/".join(pwd.split("/")[:-1])
                else:
                    if pwd == "/":
                        pwd += cmds[2]
                    else:
                        pwd += "/"+cmds[2]
                if pwd not in dir:
                    dir[pwd] = []
        else:
            cmds = line.split()
            if cmds[0] == "dir":
                # dir[pwd+"/"+cmds[0]] = []
                pass
            else:
                dir[pwd].append({"size": int(cmds[0]), "name": cmds[1]})

    odp = 0
    for d in dir:
        size = find_size(d)
        if size < 100000:
            odp += size
    return odp


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
