#!/usr/bin/env python
import sys
from typing import List


def parse_platform(lines:List[str]) -> List[List[str]]:
    result:List[List[str]] = list()

    for line in lines:
        row:List[str] = [c for c in line]
        result.append(row) # type: ignore
    return result

def roll_rock(platform:List[List[str]], x:int, y:int, dx:int, dy:int, stop_x:int, stop_y:int):
    while x+dx != stop_x and y+dy != stop_y and platform[y+dy][x+dx] == ".":
        platform[y+dy][x+dx] = "O"
        platform[y][x] = "."
        x += dx
        y += dy

def tip_platform_north(platform:List[List[str]]) -> List[List[str]]:
    row = 0
    while row < len(platform):
        col = 0
        while col < len(platform[0]):
            if platform[row][col] == "O":
                roll_rock(platform, col, row, 0, -1, -1, -1)
            col += 1
        row += 1
    return platform

def platform_north_load(platform:List[List[str]]) -> int:
    sum = 0
    row = 0
    while row < len(platform):
        col = 0
        while col < len(platform[0]):
            if platform[row][col] == "O":
                sum += len(platform) - row
            col += 1
        row += 1
    return sum

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
    platform:List[List[str]] = parse_platform(lines)
    north_plat:List[List[str]] = tip_platform_north(platform)
    result:int = platform_north_load(north_plat)
    print(f"Platform north beam load {result}")


if __name__=="__main__":
    main()
