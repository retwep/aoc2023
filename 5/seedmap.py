#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple

class Map:
    def __init__(self, name:str, maps:List[List[int]] ):
        self.name = name
        self.maps = maps

    def map(self, value:int) -> int:
        for map in self.maps:
            dest = map[0]
            src = map[1]
            run = map[2]
            if src <= value < (src+run):
                dist = value - src
                target = dest + dist
                return target
        return value


def test():

    map = Map("test1", [[100, 10, 10], [70, 30, 3]])
    values = [
        (5,5),
        (10,100),
        (20,20),
        (21,21),
        (29,29),
        (30,70),
        (32,72),
        (33,33),
        (34,34),
    ]
    for pair in values:
        m = map.map(pair[0])
        print(f"in={pair[0]} out={m}")
        assert m == pair[1]

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]

if __name__=="__main__":
    main()
