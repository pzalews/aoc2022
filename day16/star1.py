
from __future__ import annotations
from typing import List
import argparse
import os.path
import copy
from _pytest.python import show_fixtures_per_test
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

GRAPH = {}


def calculate_flow(path):
    flow = 0
    flow_step = 0
    graph = copy.deepcopy(GRAPH)
    for a in range(1, len(path)):
        if a <= 30:
            flow += flow_step
        if path[a] == path[a-1] and not graph[path[a]]["enabled"]:
            graph[path[a]]["enabled"] = True
            flow_step += GRAPH[path[a]]["rate"]

    return flow


def shortest_path(point1, point2, path) -> List[str]:
    path = path + [point1]
    if point1 == point2:
        return path
    if point1 not in GRAPH:
        return []
    shortest = []
    for node in GRAPH[point1]["dest"]:
        if node not in path:
            newpath = shortest_path(node, point2, path)
            if newpath:
                if len(shortest) == 0 or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def step(point, path, graph):
    # path = path + [point]
    # print(f"step({point},{path}")
    if point not in GRAPH:
        return []
    if len(path) >= 30:
        return [path]

    # calculate all good path (to closed velves)
    options = []
    for n in graph:
        if not graph[n]["enabled"]:
            options.append(n)
    # print(f"options={options}")
    if len(options) == 0:
        for _ in range(len(path), 31):
            path.append(point)
        return [path]
    paths = []
    for o in options:
        graph2 = copy.deepcopy(graph)
        graph2[o]["enabled"] = True
        newpath = path+shortest_path(point, o, [])
        newpaths = step(o, newpath, graph2)
        paths.extend(newpaths)
    return paths


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        tab = line.split()
        name = tab[1]
        rate = int(str(tab[4])[5:-1])
        dest = "".join(tab[9:]).split(",")
        GRAPH[name] = {"rate": rate, "dest": dest, "enabled": False}
        if rate == 0:
            GRAPH[name]["enabled"] = True
    # print(shortest_path('AA', 'DD', []))

    graph = copy.deepcopy(GRAPH)
    result = step("AA", [], graph)
    # result = [x[1:] for x in result]
    # print("RESULT")
    # print(result)
    # for r in result:
    #     print(r)

    flows = [calculate_flow(p[1:]) for p in result]
    # print("FLOWS:")
    # for f in flows:
    #     print(f)
    maximum = max(flows)
    path_nr = flows.index(maximum)
    print(result[path_nr])
    print(len(result[path_nr]))

    print(maximum)
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


# def test_shortest_path():
#     assert shortest_path("AA", "BB", []) == ["AA", "BB"]


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
