#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple



def test():
    print("Test passed")

def parse_card(line:str) -> List[int]:
    raw = line.split()
    pipe = raw.index("|")
    winning = raw[2:pipe]
    game = raw[pipe+1:]
    return winning, game

def scratch_card(winning : List[int], game:List[int]) -> int:
    score = 0
    for win in winning:
        if win in game:
            if score:
                score *= 2
            else:
                score = 1
    return score


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]

    cards = list()
    total = 0
    for line in lines:
        winning, game = parse_card(line)
        wins = scratch_card(winning, game)
        total += wins
    print(f"sum of winning scores: {total}")

if __name__=="__main__":
    main()
