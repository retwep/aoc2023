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
    count = 0
    for win in winning:
        if win in game:
            count += 1
    return count


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]

    multiples = [1 for _ in lines]
    total = 0
    for i, line in enumerate(lines):
        winning, game = parse_card(line)
        for m in range(0,multiples[i]):
            wins = scratch_card(winning, game)
            if wins:
                for j in range(0,wins):
                    multiples[i+j+1] += 1
    total = sum(multiples)
    print(f"count of cards: {total}")

if __name__=="__main__":
    main()
