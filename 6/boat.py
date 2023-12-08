#!/usr/bin/env python

import sys

# part1 = 281600
# part2 = [33875953]

def boat_race(push, limit):
    travel = limit - push
    speed = push
    distance = travel * speed
    return distance

def count_win_variations(total_time, distance_to_beat):
    win_count = 0
    for i in range(0,total_time):
        distance = boat_race(i, total_time)
        if distance > distance_to_beat:
            win_count += 1
    return win_count

def all_races(lines, no_spaces):
    if no_spaces:
        times = [int("".join(lines[0].split(" ")[1:]))]
        distances = [int("".join(lines[1].split(" ")[1:]))]
    else:
        times = [int(x) for x in lines[0].split(" ")[1:] if x != ""]
        distances = [int(x) for x in lines[1].split(" ")[1:] if x != ""]

    wins = list()
    for t,d in zip(times,distances):
        wins.append(count_win_variations(t,d))
    return wins

def product(items):
    if len(items) == 0:
        return 0
    p = items[0]
    for i in items[1:]:
        p *= i
    return p

def test():
    assert product([]) == 0
    assert product([2]) == 2
    assert product([3,4]) == 12

    for race in [(1,1,0), (1,2,1), (3,5,6)]:
        d = boat_race(race[0], race[1])
        assert  d == race[2], f"{d=}, {race=}"

    for t,d,w in [(3,1,2), (1,1,0), (7,9,4), (15,40,8), (30,200,9)]:
        wins = count_win_variations(t,d)
        assert wins == w, f"Failed: {t=}, {d=}, {w=}, {wins=}"

    print("Test passed")


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    wins = all_races(lines,False)
    result = product(wins)
    print(f"part1 = {result}")
    wins_ns = all_races(lines, True)
    print(f"part2 = {wins_ns}")

if __name__=="__main__":
    main()
