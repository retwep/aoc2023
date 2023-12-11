#!/usr/bin/env python
import sys
from typing import List

class Galaxy:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Space:
    def __init__(self, space: List[List[str]], expansion:int):
        self.space = space
        self.row_cost = self.get_row_costs(expansion)
        self.col_cost = self.get_col_costs(expansion)
        self.galaxies: List[Galaxy] = list()

    def initialize_distance_map(self):
        result = [[ 1 for _ in row] for row in self.space]
        return result

    def get_row_costs(self, expansion: int) -> List[int]:
        costs : List[int] = list()
        for r in range(0,len(self.space)):
            if self.row_is_empty(r):
                costs.append(expansion)
            else:
                costs.append(1)
        return costs
    def get_col_costs(self, expansion: int) -> List[int]:
        costs : List[int] = list()
        for c in range(0,len(self.space[0])):
            if self.col_is_empty(c):
                costs.append(expansion)
            else:
                costs.append(1)
        return costs

    def row_is_empty(self, row: int) -> bool:
        for x in self.space[row]:
            if x != ".":
                return False
        return True

    def col_is_empty(self, col: int) -> bool:
        for row in self.space:
            if row[col] != ".":
                return False
        return True

    def find_all_galaxies(self):
        self.galaxies: List[Galaxy] = list()
        for y,row in enumerate(self.space):
            for x,col in enumerate(row):
                if col == "#":
                    self.galaxies.append(Galaxy(x,y))
    
    def distance(self, g1:Galaxy, g2:Galaxy) -> int:
        total:int = 0
        y1 = min(g1.y, g2.y)
        y2 = max(g1.y, g2.y)

        for r in range(y1, y2):
            total += self.row_cost[r]
        x1 = min(g1.x, g2.x)
        x2 = max(g1.x, g2.x)
        for c in range(x1, x2):
            total += self.col_cost[c]
        return total

    def measure_distances(self) -> int:
        self.find_all_galaxies()
        total:int = 0
        for i in range(0,len(self.galaxies)-1):
            for j in range(i,len(self.galaxies)):
                total += self.distance(self.galaxies[j], self.galaxies[i])
        return total
        

def test():


    print("Test passed")

def parse_space(lines: List[str], expansion: int) -> Space:
    result:List[List[str]] = list()
    for line in lines:
        result.append([c for c in line])
    space = Space(result, expansion)
    return space

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    expansion = int(sys.argv[2])
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    space = parse_space(lines, expansion)
    total: int = space.measure_distances()
    print(f"Sum of distances {total}")


if __name__=="__main__":
    main()
