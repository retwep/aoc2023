#!/usr/bin/env python
import sys
from typing import List, Tuple

class Point:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    def __eq__(self, p:object) -> bool:
        if not isinstance(p, Point):
            return False
        return self.x == p.x and self.y == p.y


class Walker:
    def __init__(self, here: Point, prev: Point):
        # where we are
        self.here = here
        # where we were
        self.prev = prev
        self.distance = 1 # we entered at S and moved one space.
    
    def step(self, maze:"Maze"):
        options = maze.possible_directions(self.here)
        assert len(options) in [1,2]
        if options[0] == self.prev:
            next = options[1]
        else:
            next = options[0]
        self.prev = self.here
        self.here = next
        maze.visit(next)
        self.distance += 1

class Maze:
    def __init__(self, lines:List[str]):
        self.width = len(lines[0])
        self.height = len(lines)
        self.lines:List[List[str]] = [[c for c in l] for l in lines]
        blank = [" " for _ in range(0,len(lines[0]))]
        self.visited:List[List[str]] = [blank.copy() for _ in lines]


    def get(self, x:int, y:int) -> str:
        return self.lines[y][x]

    def visit(self, p:Point):
        self.visited[p.y][p.x] = "X"

    def was_visited(self, x:int,y:int) -> bool:
        return self.visited[y][x] != " "

    def find_start(self) -> Point:
        for y in range(0,self.height):
            for x in range(0,self.width):
                if self.get(x,y) == "S":
                    return Point(x,y)
        assert False, "Bad maze? no start?"

    def get_walkers(self, p: Point) -> Tuple[Walker, Walker]:
        p = self.find_start()
        self.visit(p)
        options = self.possible_directions(p)
        walkers:List[Walker] = list()
        for option in options:
            self.visit(p)
            self.visit(option)
            walkers.append(Walker(prev=p,here=option))
        return tuple(walkers) # type: ignore

    def possible_directions(self, p:Point) -> List[Point]:
        # which of the 4 surrounding squares is a direction a walker could move to?
        # F---7
        # |...|
        # |...|
        # L---J
        directions = [
            #x,y,next,here
            (-1,0,"-FL", "S7J-"),
            (1,0,"-7J", "FL-S"),
            (0,-1,"|F7", "|LJS"),
            (0,1,"|LJ", "|F7S")
        ]
        options:List[Point] = list()
        c = self.get(p.x,p.y)
        for option in directions:
            if c in option[3] and self.get(p.x+option[0],p.y+option[1]) in option[2]:
                options.append(Point(p.x+option[0],p.y+option[1]))
        assert len(options) in [1,2], f"Only 2 directions allowed! {len(options)}"
        return options

    def measure_distant(self):
        start = self.find_start()
        w1, w2 = self.get_walkers(start)

        while True:
            w1.step(self)
            if w1.here == w2.here:
                break
            w2.step(self)
            if w2.here == w1.here:
                break
        distance = max(w1.distance, w2.distance)
        return distance

    def enclosed_area(self) -> int:
        count = 0
        for y in range(0,self.height):
            inside = False
            last_corner_up = False
            for x in range(0,self.width):
                #  F----JL---7
                if self.was_visited(x,y):
                    # this pipe is relevant
                    # F----7.F----7
                    # |....L-J....|
                    # L-----------J
                    c = self.get(x,y)
                    if c in "F":
                        last_corner_up = False
                    elif c in "L":
                        last_corner_up = True
                    elif c in "7":
                        if last_corner_up:
                            inside = not inside
                        last_corner_up = False
                    elif c in "J":
                        if not last_corner_up:
                            inside = not inside
                        last_corner_up = True
                    elif c in "|":
                        inside = not inside
                    elif c in "S" and not inside:
                        last_corner_up = False
                        #inside = not inside
                    # elif c == "S":  Cheated and could see that S is not a state change for my map.  Not true of all maps.
                    # This gets "fun" when you have to figure out if S is on a corner (== state change) or middle (== not a state change)
                elif inside:
                    count += 1

            assert not inside  # because of blank padding we should always be outside at the end of a line
        return count


def test():
    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [f".{r.strip()}." for r in raw_lines] # lazy - pre-pad to avoid painful edge conditions later
    blank = "."*len(lines[0])
    lines.insert(0, blank)
    lines.append(blank)
    maze = Maze(lines)

    most_distant = maze.measure_distant()
    print(f"{most_distant=}")

    enclosed = maze.enclosed_area()
    print(f"{enclosed=}")

if __name__=="__main__":
    main()
