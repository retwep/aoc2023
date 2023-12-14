#!/usr/bin/env python
import copy
import sys
from typing import Any, List, Union


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

def tip_platform_south(platform:List[List[str]]) -> List[List[str]]:
    row = len(platform)-1
    while row >= 0:
        col = 0
        while col < len(platform[0]):
            if platform[row][col] == "O":
                roll_rock(platform, col, row, 0, 1, len(platform[0]), len(platform))
            col += 1
        row -= 1
    return platform

def tip_platform_west(platform:List[List[str]]) -> List[List[str]]:
    col = 0
    while col < len(platform[0]):
        row = 0
        while row < len(platform):
            if platform[row][col] == "O":
                roll_rock(platform, col, row, -1, 0, -1, -1)
            row += 1
        col += 1
    return platform

def tip_platform_east(platform:List[List[str]]) -> List[List[str]]:
    col = len(platform[0])-1
    while col >= 0:
        row = 0
        while row < len(platform):
            if platform[row][col] == "O":
                roll_rock(platform, col, row, 1, 0, len(platform[0]), len(platform))
            row += 1
        col -= 1
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

def equals(a:List[List[str]], b:List[List[str]]) -> bool:
    for av, bv in zip(a,b):
        if av != bv:
            return False
    return True

def find_match(cycles:List[List[List[str]]], platform:List[List[str]]) -> int:
    i:int = len(cycles)-1
    while i >= 0:
        if equals(cycles[i], platform):
            return i
        i -= 1
    return i

def test():
    inputs = [
        ("12123"*20, 5),
        ("1212"*20, 2),
        ("1112223331112223337"*20, 19),
        ("1234567890", None),
    ]
    for input in inputs:
        x = [c for c in input[0]]
        n = find_longest_shortest_pattern(x)
        assert n == input[1], f"Fail: {n=}, {input[1]=}, {input[0]=}"

    print("Test passed")

def show(platform:List[List[str]]):
    print("#####################################\n")
    for i,row in enumerate(platform):
        print(f'{len(platform)-i:2} {"".join(row)}')
    print("#####################################\n")

def find_longest_shortest_pattern(v:List[Any]) -> Union[int, None]:
    check_copies = 5  # pattern must repeat at least this number of time before we call it a pattern
    x = v.copy()
    x.reverse()
    if not x or len(x) < 5:
        return None
    pattern:List[int] = list()
    pattern.append(x[0])
    while True:
        offset = 0
        for _ in range(check_copies):
            for p in pattern:
                if x[offset] != p:
                    pattern = x[0:offset+1]
                    if len(pattern) >= len(x):
                        return None
                    offset = 0
                    break
                offset += 1
            if offset == 0:
                break
        else:
            return len(pattern)
    return None


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    platform:List[List[str]] = parse_platform(lines)
    cycles:List[List[List[str]]] = list()
    loads:List[int] = list()
    #cycle_plat = copy.deepcopy(platform)
    #cycles.append(cycle_plat)
    iterations = 0
    hard_stop = 1000000000
    m = hard_stop # initialize for linter
    print("Original")
    show(platform)
    while iterations < hard_stop:
        print("North")
        tip_platform_north(platform)
        show(platform)

        print("West")
        tip_platform_west(platform)
        show(platform)

        print("South")
        tip_platform_south(platform)
        show(platform)

        print("East")
        tip_platform_east(platform)
        show(platform)

        cycle_plat = copy.deepcopy(platform)
        cycles.append(cycle_plat)

        result:int = platform_north_load(platform)
        print(f"Platform north beam load {result} after {len(cycles)} cycles")
        loads.append(result)

        m = find_match(cycles, platform)
        print(f"{iterations=}, {m=}")
        if m > 0 and iterations > 1000:
            break
        iterations += 1

    assert m > 0
    print(f"{loads=}")

    m = find_longest_shortest_pattern(loads)
    assert m
    
    # compute the modulo of repeat pattern from here to end point to get the ending iteration, weigh it.
    remaining_iterations = 1000000000 - len(cycles)
    repeat = m
    leftovers = remaining_iterations % repeat
    final = cycles[-(m-leftovers+1)]
    result:int = platform_north_load(final)
    print(f"Platform north beam load {result} after {hard_stop} cycles, with cycle repeat {repeat}")


if __name__=="__main__":
    main()
