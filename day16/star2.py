
from __future__ import annotations
import functools
from typing import List
import argparse
import os.path
import copy
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

GRAPH = {}


@functools.lru_cache(maxsize=None)
def calculate_flow(path):
    flow = 0
    flow_step = 0
    graph = copy.deepcopy(GRAPH)
    for a in range(1, 27):
        flow += flow_step
        if a < len(path) and path[a] == path[a-1] and not graph[path[a]]["enabled"]:
            graph[path[a]]["enabled"] = True
            flow_step += graph[path[a]]["rate"]

    return flow


@functools.lru_cache(maxsize=None)
def shortest_path(point1, point2, path) -> List[str]:
    path = list(path) + [point1]
    if point1 == point2:
        return path
    if point1 not in GRAPH:
        return []
    shortest = []
    for node in GRAPH[point1]["dest"]:
        if node not in path:
            newpath = shortest_path(node, point2, tuple(path))
            if newpath:
                if len(shortest) == 0 or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def step(path1, path2, graph):
    if len(path1) > len(path2):
        path = path2
        opath = path1
    else:
        path = path1
        opath = path2
    if len(path) > 0:
        point = path[-1]
    else:
        point = "AA"
    if point not in GRAPH:
        return [([], [])]
    if len(path) >= 26:
        return [(path1, path2)]

    # calculate buisnes value
    values = {}
    for n in graph:
        if not graph[n]["enabled"]:
            dist = len(shortest_path(point, n, tuple([])))

            if dist > 0:
                steps = 27-len(path)-dist-1
                if steps > 0:
                    rate = (graph[n]["rate"] * steps)
                    # rate = (graph[n]["rate"] * steps)/dist
                    values[n] = rate
    maximum = 0
    for v in values:
        if values[v] > maximum:
            maximum = values[v]
    options = []
    for v in values:
        # if values[v] > maximum//2:
        if values[v] > 0 and values[v] > maximum//4:
            options.append(v)
    # print(f"options:{options}")
    if len(options) == 0:
        for _ in range(len(path), 27):
            path = list(path)
            path.append(point)
        return step(path, opath, graph)
    paths = []
    for o in options:
        graph2 = copy.deepcopy(graph)
        graph2[o]["enabled"] = True
        npath = list(path)+shortest_path(point, o, tuple([]))
        newpaths = step(opath, npath, graph2)
        # print(newpaths)
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
    print(shortest_path('AA', 'BB', tuple([])))

    graph = copy.deepcopy(GRAPH)
    result = step([], [], graph)
    print("RESULT")
    # print(result)
    # for r in result:
    #      print(r)

    flows = [calculate_flow(tuple(p[0]))+calculate_flow(tuple(p[1]))
             for p in result]
    print("FLOWS:")
    # for f in flows:
    #     print(f)
    maximum = max(flows)
    print("Max:"+str(maximum))
    index = flows.index(maximum)
    print(result[index])
    print(
        f"{calculate_flow(tuple(result[index][0]))} + {calculate_flow(tuple(result[index][1]))}")

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
EXPECTED = 1707


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
