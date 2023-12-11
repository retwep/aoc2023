#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple

def row_is_empty(row: List[str]) -> bool:
    for x in row:
        if x != ".":
            return False
    return True

def col_is_empty(space: List[List[str]], col: int) -> bool:
    for row in space:
        if row[col] != ".":
            return False
    return True

def expand(space:List[List["str"]]) -> List[List[str]]:
    width = len(space[0])
    height = len(space)
    # expand for empty rows
    exp:List[List[str]] = list()
    for row in range(0,height):
        exp.append(space[row].copy())
        if row_is_empty(space[row]):
            exp.append(space[row].copy())
    
    # for columns, scan to build the list then expand in second pass.
    cols:List[int] = list()
    for col in range(0,width):
        if col_is_empty(space, col):
            cols.append(col)
    cols.reverse()
    for row in exp:
        for col in cols:
            row.insert(col, ".")
    return exp

class Galaxy:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

def find_all_galaxies(space:List[List[str]]) -> List[Galaxy]:
    galaxies: List[Galaxy] = list()
    for y,row in enumerate(space):
        for x,col in enumerate(row):
            if col == "#":
                galaxies.append(Galaxy(x,y))
    return galaxies

def measure_distances(space:List[List[str]]) -> int:
    galaxies = find_all_galaxies(space)
    total = 0
    for i in range(0,len(galaxies)-1):
        for j in range(i,len(galaxies)):
            total += abs(galaxies[j].x-galaxies[i].x) + abs(galaxies[j].y - galaxies[i].y)
    return total


def test():
    raw = [["."]]
    out = expand(raw)
    assert len(out) == 2
    assert len(out[0]) == 2
    raw = [[".","#"]]
    out = expand(raw)
    assert len(out) == 1
    assert len(out[0]) == 3
    raw = [
        [".",".","#"],
        [".",".","."],
        ["#",".","."],
        [".",".","."],
        ]
    out = expand(raw)
    assert len(out) == 6
    assert len(out[0]) == 4


    print("Test passed")

def parse_space(lines: List[str]) -> List[List[str]]:
    result:List[List[str]] = list()
    for line in lines:
        result.append([c for c in line])
    return result

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    space = parse_space(lines)
    bigger = expand(space)

    total = measure_distances(bigger)
    print(f"Sum of distances {total}")


if __name__=="__main__":
    main()
