#!/usr/bin/env python

# part1 submission 1 12083

import sys
from typing import Dict, List, Tuple

def navigate(turns:str, map:Dict[str,Dict[str,str]]) -> int:
    tm = len(turns)
    count = 0
    here = "AAA"

    while here != "ZZZ":
        turn = turns[count % tm]
        count += 1
        here = map[here][turn]
    return count

def load_map(lines:List[str]) -> Tuple[str,Dict[str,Dict[str,str]]]:
    directions = lines[0]
    map = dict()
    for line in lines[2:]:
        line = line.replace(" ", "")
        key, t = line.split('=')
        t = t.split(',')
        left = t[0][1:]
        right = t[1].strip()[:-1]
        assert key not in map
        map[key] = {"L":left,"R":right}
    print(f"Map has {len(directions)} turns and {len(map)} keys")
    return directions, map

def test():
    d,m = load_map(["L", "", "AAA = (ZZZ,AAA)"])
    assert d == "L"
    assert m == {"AAA": {"L": "ZZZ", "R":"AAA"}}

    turns = navigate(d, m)
    assert turns == 1
    d = "LLR"
    m = {"AAA": {"L":"B", "R":"Z"},
         "B": {"L":"C", "R":"Z"},
         "C": {"L":"Z", "R":"D"},
         "D": {"L":"E", "R":"Z"},
         "E": {"L":"F", "R":"Z"},
         "F": {"L":"Z", "R":"ZZZ"},
         "Z": {"L":"Z", "R":"Z"},
         }
    turns = navigate(d,m)
    assert turns == 6

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    d,m = load_map(lines)
    turns = navigate(d,m)
    print(f"map took {turns=}")

if __name__=="__main__":
    main()
