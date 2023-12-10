#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple

class Run:
    def __init__(self, start, len):
        self.start = start
        self.len = len
        self.finish = start+len-1

    def inside(self, value):
        return self.start <= value and self.finish >= value

class Translation:
    def __init__(self, dest, run: Run): 
        self.dest = dest
        self.run

    @staticmethod
    def sort(translations: List["Translation"]):
        result = sorted(translations, key=lambda x:x.run.start)
        return result


class Transformation:
    def __init__(self, name:str, maps:List[Translation] ):
        self.name = name
        self.translations = maps
        self.sort()

    def sort(self):
        for i,t in enumerate(self.translations):
            s = Translation.sort(t)
            self.translations[i] = s

    def map(self, value:int) -> int:
        for map in self.translations:
            dest = map.dest
            src = map.run.start
            run = map.run.run
            if src <= value < (src+run):
                dist = value - src
                target = dest + dist
                return target
        return value


    @staticmethod
    def flatten_maps(transforms: List["Transformation"]):
        for t in transforms:
            # pairwise go through the transforms and combine them to create a single transform from input to output.
            TODO: start here, take pairs of transforms and flatten them
            



def test():

    map = Transformation("test1", [[100, 10, 10], [70, 30, 3]])
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

def parse_lines(lines:List[str]) -> Tuple[List[int], List[Transformation]]:
    assert "seeds" in lines[0]
    raw_seeds = lines[0].split()
    seeds = [int(v) for v in raw_seeds[1:]]

    # part 2 treats seeds as a range of values - split them
    seeds = list()
    for s in range(0,len(sv), 2):
        r = Run(sv[s], sv[s+1])

    maps = list()
    map_translations = list()
    name = ""
    def add_map():
        nonlocal maps, name, map_translations
        if map_translations:
            map = Transformation(name, map_translations)
            maps.append(map)
            map_translations = list()
            name = ""
        
    for line in lines[1:]:
        if "map" in line:
            add_map()
            name = line.split()[0] # puzzle doesn't need this but may help for debugging
        elif line:
            raw = line.split()
            t = Translation(raw[0], Run(raw[1], raw[2])) # will be too hard to think with flat [dest,src,len,dest,src,len,dest,src,len]
            map_translations.append(t)
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

    # create a single translation mapping from multiple sub-mappings
    flat = Transformation.flatten_maps(maps)

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
