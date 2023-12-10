#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple


class Run:
    """This puzzle has multiple areas with a start and length, seeds, and translation ranges between domains."""

    def __init__(self, first, len):
        self.first = first
        self.len = len
        self.last = first+len-1 # inclusive, which isn't python typical
    
    # possible relationship between 2 runs:
    DISJOINT=0  # no overlap
    START_OVERLAP=1  # self.first is inside the run, but self.last is outside the run
    END_OVERLAP=2  # self.fist is outside the run, but self.last is inside the run
    CONTAINED=3  # self.first and self.last are both inside the run
    INSIDE=4  # entire run is between self.first and self.last
    def contains(self, run):
        # result is relative to self.
        if self.first > run.last or self.last < run.first:
            return Run.DISJOINT

        # this feels like it is too much - do I really need all this crap?
        if run.first < self.first and run.last > self.last:
            return Run.CONTAINED
        if run.first < self.first and run.last <= self.last:
            return Run.START_OVERLAP
        if run.first >= self.first and run.last <= self.last:
            return Run.INSIDE
        if run.first >= self.first and run.last > self.last:
            return Run.END_OVERLAP
        assert False, "we should have hit it before here"
    
    def split(self, where) -> "Run":
        assert where > self.first, "you've got a bug -- should never split before the range"
        assert where <= self.last, "you've got a bug -- should never split after the range"
        new_len = self.len - (where-self.first)
        new_run = Run(where, new_len)
        self.len = where-self.first
        return new_run

class Translation:  # translate segment from one number domain to the next
    def __init__(self, dest: int, run:Run):
        self.dest = dest
        self.run = run

    def translate(self, run:Run) ->List[Run]:
        # Given a run of values, translate it


class Domain:
    """each src->dest mapping is a translation domain"""
    def __init__(self, name:str, maps:List[Translation] ):
        self.name = name
        self.maps = sorted(maps, key=lambda x:x.run.first) # later algos require the map list to be cleanly sorted.

    def translate(self, run: Run) -> List[Run]:
        # a run in, maybe more than one run out

        for map in self.maps:
            # possible conditions:
            # Disjoint (run and map don't overlap)
            # rrr
            #     mmm 
            overlap = map.run.contains(run)
            if overlap == Run.DISJOINT:
                continue

            # 
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
    sv, maps = parse_lines(lines)

    # part 2 treats seeds as a range of values - split them
    seeds = list()
    for s in range(0,len(sv), 2):
        r = Run(sv[s], sv[s+1])

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
