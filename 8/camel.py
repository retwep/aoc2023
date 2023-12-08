#!/usr/bin/env python

import sys
from typing import Dict, List, Tuple

def navigate(turns:str, map:Dict[str,Dict[str,str]]) -> int:
    tm = len(turns)
    count = 0
    here = next(iter(map))
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
        map[key] = {"L":left,"R":right}
    return directions, map

def test():
    d,m = load_map(["L", "", "A = (ZZZ,AAA)"])
    assert d == "L"
    assert m == {"A": {"L": "ZZZ", "R":"AAA"}}

    turns = navigate(d, m)
    assert turns == 1
    
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
