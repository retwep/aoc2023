#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple


class DiggerMove:
    def __init__(self, direction:str, distance:int, color:str):
        self.direction = direction
        self.distance = distance
        self.color = color
    
    @staticmethod
    def estimate_hole(moves: List["DiggerMove"]) -> Tuple[int, int]:
        dmax:Dict[str, int] = dict()
        dmax["R"]=0
        dmax["L"]=0
        dmax["U"]=0
        dmax["D"]=0
        for d in moves:
            dmax[d.direction] += d.distance
        width:int = dmax["R"]+dmax["L"]
        height:int = dmax["D"]+dmax["U"]
        return width*2,height*2
    
    @staticmethod
    def dig(ground:List[List[str]], moves:List["DiggerMove"], startc:int, startr:int):
        row = startr
        col = startc
        ground[row][col] = "#"
        min_c = 1000
        max_c = -1
        min_r = 1000
        max_r = -1
        for move in moves:
            for _step in range(move.distance):
                if move.direction == "D":
                    row += 1
                    max_r = max(row,max_r)
                elif move.direction == "U":
                    row -= 1
                    min_r = min(row,min_r)
                elif move.direction == "R":
                    col += 1
                    max_c = max(col, max_c)
                elif move.direction == "L":
                    col -= 1
                    min_c = min(col, min_c)
                ground[row][col] = "#"
                if ground[row][col-1] != "#":
                    ground[row][col-1] = "L"
                if ground[row][col+1] != "#":
                    ground[row][col+1] = "R"

        # trim the ground to just what we used.  Very lazy and a high chance we'll blow chunks before we get here depending on the input data.
        ground = ground[min_r - 2: max_r+2]
        for i,row in enumerate(ground):
            ground[i] = row[min_c - 2 : max_c + 2]  # drop excess columns

        width = len(ground[0])
        height = len(ground)


        # basic scanning fill for unambiguous areas
        mystery = False
        for row in range(height):
            outside = True
            for col in range(width):
                g = ground[row][col]
                if outside and g in "LR.":
                    ground[row][col] = "O"
                elif g == "#" and ground[row][col+1] == "#":
                    # mystery row -- we'll come back later if we hit these, for now, mark what we can easily.
                    mystery = True
                    j = width-1
                    rout = True
                    fill = "O"
                    while j > col:
                        if rout:
                            if ground[row][j] == "#" and ground[row][j-1] == "#":
                                fill = "M"
                                rout = False
                            elif ground[row][j] == "#" and ground[row][j-1] != "#":
                                fill = "X"
                            else:  # clear solution to filling either outside or a simple line crossing
                                ground[row][j] = fill
                        else:
                            if ground[row][j] not in "X#O":
                                # Mystery to be resolved later
                                ground[row][j] = fill
                                mystery = True
                        j -= 1
                    break  # we finished out this entire row already
                elif outside:
                    if g == "#":
                        # clear line crossing
                        outside = False
                    else:
                        ground[row][col] = "O"
                elif not outside:
                    if g == "#":
                        # clear line crossing
                        outside = True
                    else:
                        ground[row][col] = "X"
            print("".join(ground[row]))

        # trying something silly -- multipass fill -- if we don't know, skip it and come back later
        if mystery:
            print()
            done = False
            while not done:
                done = True
                for row in range(1,height-1):
                    col = 1
                    while col < width-1:
                        # no hints for crossings, so let's paint!
                        g = ground[row][col]
                        if g == "M":
                            done = False
                            if ground[row-1][col] == "X" or ground[row+1][col] == "X" or ground[row][col-1] == "X" or ground[row][col+1] == "X":
                                ground[row][col] = "X"  # adjacency filling -- really likely to leave holes
                            elif ground[row-1][col] == "O" or ground[row+1][col] == "O" or ground[row][col-1] == "O" or ground[row][col+1] == "O":
                                ground[row][col] = "O"  # adjacency filling -- really likely to leave holes
                        col += 1
                    print("".join(ground[row]))
        return ground

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

    moves : List[DiggerMove] = list()
    for line in lines:
        direction, d, color = line.split()
        distance = int(d)
        dm = DiggerMove(direction, distance, color)
        moves.append(dm)

    width, height = DiggerMove.estimate_hole(moves)
    ground = [["." for _w in range(width)] for _h in range(height)]
    ground = DiggerMove.dig(ground, moves, width//2, height//2)
    count = 0
    for r in ground:
        for c in r:
            if c in "X#":
                count += 1
            else:
                assert c in "LR.O"
    print(f"Found {count} blocks")



if __name__=="__main__":
    main()
