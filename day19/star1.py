
from __future__ import annotations

import argparse
import os.path

import pytest

import support
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

BLUEPRINTS = []


def quality_metric(state):
    ((ore, clay, obsidian, geodes), (ore_robot, clay_robot,
     obsidian_robot, geode_robot), time) = state
    return ore+clay*10+obsidian*100+geodes*1000+ore_robot*5+clay_robot*50+obsidian_robot*500+geode_robot*5000


def blueprint_process(blueprint):
    best = 0
    # State ((ore,clay,obsidian,geodes),(ore_robot, clay_robot, obsidian_robot,geode_robot),time)
    start = ((0, 0, 0, 0), (1, 0, 0, 0), 0)
    Q = list()
    Q.append(start)
    CACHE = set()
    depth = 0
    T = 24
    while Q:
        state = Q.pop(0)
        ((ore, clay, obsidian, geodes), (ore_robot, clay_robot,
         obsidian_robot, geode_robot), time) = state
        best = max(best, geodes)
        # print((time, ore_robot, clay_robot, obsidian_robot,
        #       geode_robot, ore, clay, obsidian, geodes))
        # breakpoint()
        if time == T:
            continue

        # optimalization
        # max_ore_use = max([blueprint["ore_robot"], blueprint["clay_robot"],
        #                   blueprint["obsidian_robot"][0],
        #                    blueprint["geode_robot"][0]])
        # if ore_robot >= max_ore_use:
        #     ore_robot = max_ore_use
        # if clay_robot >= blueprint["obsidian_robot"][1]:
        #     clay_robot = blueprint["obsidian_robot"][1]
        # if obsidian_robot > - blueprint["geode_robot"][1]:
        #     obsidian_robot = blueprint["geode_robot"][1]
        state = ((ore, clay, obsidian, geodes),
                 (ore_robot, clay_robot, obsidian_robot, geode_robot), time)
        if state in CACHE:
            continue
        CACHE.add(state)
        # clean table
        if time > depth:
            Q.sort(key=quality_metric, reverse=True)
            Q = Q[:10000]
            depth = depth+1
            # print(f"{time} {len(CACHE)} {best}")

        state = ((ore+ore_robot, clay+clay_robot,
                  obsidian+obsidian_robot, geodes+geode_robot),
                 (ore_robot, clay_robot, obsidian_robot, geode_robot), time+1)
        Q.append(state)
        # if we could buy robot lets try what happen if we buy
        if ore >= blueprint["ore_robot"]:
            state = ((ore+ore_robot-blueprint["ore_robot"], clay+clay_robot,
                      obsidian+obsidian_robot, geodes+geode_robot),
                     (ore_robot+1, clay_robot, obsidian_robot, geode_robot),
                     time+1)
            Q.append(state)
        if ore >= blueprint["clay_robot"]:
            state = ((ore+ore_robot - blueprint["clay_robot"], clay+clay_robot,
                      obsidian+obsidian_robot, geodes+geode_robot),
                     (ore_robot, clay_robot+1, obsidian_robot, geode_robot),
                     time+1)
            Q.append(state)
        if (ore >= blueprint["obsidian_robot"][0] and
                clay >= blueprint["obsidian_robot"][1]):
            state = ((ore+ore_robot - blueprint["obsidian_robot"][0],
                      clay+clay_robot - blueprint["obsidian_robot"][1],
                      obsidian+obsidian_robot, geodes+geode_robot),
                     (ore_robot, clay_robot, obsidian_robot+1, geode_robot),
                     time+1)
            Q.append(state)
        if (ore >= blueprint["geode_robot"][0] and
                obsidian >= blueprint["geode_robot"][1]):
            state = ((ore+ore_robot - blueprint["geode_robot"][0],
                      clay+clay_robot,
                      obsidian+obsidian_robot - blueprint["geode_robot"][1],
                      geodes+geode_robot),
                     (ore_robot, clay_robot, obsidian_robot, geode_robot+1),
                     time+1)
            Q.append(state)
    return best


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        c = re.findall(r'\d+', line)
        BLUEPRINTS.append({"ore_robot": int(c[1]),
                           "clay_robot": int(c[2]),
                           "obsidian_robot": [int(c[3]), int(c[4])],
                           "geode_robot": [int(c[5]), int(c[6])],
                           })
    odp = 0
    for i, b in enumerate(BLUEPRINTS):
        best = blueprint_process(b)
        print(f"SOLUTION {i} = {best}")
        odp += (i+1)*(best)
    return odp


# Blueprint 1:
#    Each ore robot costs 4 ore.
#    Each clay robot costs 2 ore.ZZ
#    Each obsidian robot costs 3 ore and 14 clay.
#    Each geode robot costs 2 ore and 7 obsidian.
INPUT_S = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''
EXPECTED = 33


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
