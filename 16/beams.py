#!/usr/bin/env python
import sys
from typing import List

DOWN=1
UP=2
LEFT=4
RIGHT=8

class Beam:
    def __init__(self, x:int,y:int, dx:int,dy:int):
        self.x = x
        self.y = y
        self.dx=dx
        self.dy=dy

def trace_beam(grid:List[List[str]], map:List[List[int]], beams:List[Beam]):
    while len(beams):
        beam:Beam = beams[0]
        beam.x += beam.dx
        beam.y += beam.dy
        if beam.x < 0 or beam.y < 0 or beam.x >= len(grid[0]) or beam.y >= len(grid):
            beams = beams[1:]
            continue

        # truncate beams if they are in the same place going the same direction
        m = map[beam.y][beam.x]
        if ((beam.dx > 0 and (m & RIGHT)) or
            (beam.dx < 0 and (m & LEFT)) or
            (beam.dy > 0 and (m & DOWN)) or
            (beam.dy < 0 and (m & UP))):
            beams = beams[1:]
            # same place, same direction
            continue

        if beam.dx > 0:
            map[beam.y][beam.x] |= RIGHT
        elif beam.dx < 0:
            map[beam.y][beam.x] |= LEFT
        elif beam.dy > 0:
            map[beam.y][beam.x] |= DOWN
        elif beam.dy < 0:
            map[beam.y][beam.x] |= UP

        c = grid[beam.y][beam.x]
        if c == ".":
            continue
        elif c == "|":
            if beam.dx == 0:
                continue
            newb = Beam(beam.x, beam.y, dx=0, dy=-1)
            beams.append(newb)
            beam.dx=0
            beam.dy=1
        elif c == "-":
            if beam.dy == 0:
                continue
            newb = Beam(beam.x, beam.y, dx=-1, dy=0)
            beams.append(newb)
            beam.dx=1
            beam.dy=0
        elif c == "/":
            d = beam.dx
            beam.dx = -beam.dy
            beam.dy = -d
        elif c == "\\":
            d = beam.dx
            beam.dx = beam.dy
            beam.dy = d
        else:
            assert False, f"Unexpected character {c} at {beam.x}, {beam.y}"

def trace_beams(grid:List[List[str]]) -> int:
    width = len(grid[0])
    height = len(grid)
    best = 0
    def count_cells(map):
        nonlocal best
        count:int = 0
        for row in map:
            for col in row:
                if col:
                    count += 1
        best = max(count, best)


    for x in range(width):
        map:List[List[int]] = [[0 for _ in l] for l in grid]
        beam = Beam(x=x, y=-1, dx=0, dy=1)
        beams:List[Beam] = [beam]
        trace_beam(grid, map, beams)
        count_cells(map)

        map:List[List[int]] = [[0 for _ in l] for l in grid]
        beam = Beam(x=x, y=height, dx=0, dy=-1)
        beams:List[Beam] = [beam]
        trace_beam(grid, map, beams)
        count_cells(map)

    for y in range(height):
        map:List[List[int]] = [[0 for _ in l] for l in grid]
        beam = Beam(x=-1, y=y, dx=1, dy=0)
        beams:List[Beam] = [beam]
        trace_beam(grid, map, beams)
        count_cells(map)

        map:List[List[int]] = [[0 for _ in l] for l in grid]
        beam = Beam(x=width, y=y, dx=-1, dy=0)
        beams:List[Beam] = [beam]
        trace_beam(grid, map, beams)
        count_cells(map)

    return best

def test():
    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    grid:List[List[str]] = [[c for c in l] for l in lines]
    energized = trace_beams(grid)
    print(f"Energized cells {energized=}")

if __name__=="__main__":
    main()
