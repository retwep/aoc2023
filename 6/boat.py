#!/usr/bin/env python

import sys

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

def all_races(lines):
    times = lines[0].split(" ")[1:]
    distances = lines[1].split(" ")[1:]
    wins = list()
    for t,d in zip(times,distances):
        wins.append(count_win_variations(t,d))
    return wins

def test():
    for race in [(1,1,0), (1,2,1), (3,5,6)]:
        d = boat_race(race[0], race[1])
        assert  d == race[2], f"{d=}, {race=}"

    for t,d,w in [(2,1,1), (1,1,0), (7,9, 4),(15,40,8),(30,200,9)]:
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
    wins = all_races(lines)
    result = prod(wins)
    print(f"{result=}")

if __name__=="__main__":
    main()
