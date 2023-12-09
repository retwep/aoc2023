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

def parse_lines(lines:List[str]) -> Tuple[List[int], List[Map]]:
    assert "seeds" in lines[0]
    raw_seeds = lines[0].split(" ")
    seeds = [int(v) for v in raw_seeds[1:] if v != ""]

    maps = list()
    map_data = list()
    name = ""
    def add_map():
        nonlocal maps, name, map_data
        if map_data:
            map = Map(name, map_data)
            maps.append(map)
            map_data = list()
            name = ""
        
    for line in lines[1:]:
        if "map" in line:
            add_map()
            name = line.split(" ")[0] # puzzle doesn't need this but may help for debugging
        elif line:
            data = [int(v) for v in line.split(" ") if v != ""]
            map_data.append(data)
    add_map()
    for map in maps:
        print(f"loaded map: {map.name}")
    return (seeds, maps)

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    seeds, maps = parse_lines(lines)

    locations = list()
    for seed in seeds:
        s = seed
        for m in maps:
            s = m.map(s)
        locations.append(s)
        print(f"{seed=}, location={s}")
    
    print(f"closest seed is {min(locations)}")

if __name__=="__main__":
    main()
