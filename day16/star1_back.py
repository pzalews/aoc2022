
from __future__ import annotations

import argparse
import os.path
import copy
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

GRAPH = {}


def calculate_flow(path):
    flow = 0
    flow_step = 0

    for a in range(1, len(path)):
        flow += flow_step
        if path[a] == path[a-1]:
            flow_step += GRAPH[a]["rate"]

    return flow


def step(point, path, graph):
    path = path + [point]
    print(f"step({point},{path}")
    if point not in GRAPH:
        return []
    p = graph[point]
    if len(path) >= 30:
        return [path]
    paths = []
    if p["rate"] == 0:
        p["enabled"] = True

    if not p["enabled"]:
        graph2 = copy.deepcopy(graph)
        graph2[point]["enabled"] = True
        print(graph2[point]["enabled"])
        print(graph[point]["enabled"])
        newpaths = step(point, path, graph2)
        for new in newpaths:
            paths.append(new)
    for node in p["dest"]:
        # graph2 = copy.deepcopy(graph)
        newpaths = step(node, path, graph)
        for new in newpaths:
            paths.append(new)
    return paths


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        tab = line.split()
        name = tab[1]
        rate = int(str(tab[4])[5:-1])
        dest = "".join(tab[9:]).split(",")
        GRAPH[name] = {"rate": rate, "dest": dest, "enabled": False}

    result = step("AA", [], GRAPH)
    # for r in result:
    #     print(r)
    flows = [calculate_flow(p) for p in result]
    # for f in flows:
    #     print(f)
    maximum = max(flows)
    return maximum


INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1651


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
