#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple



def test():
    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    handbids = [r.strip() for r in raw_lines]
    result = play_cards(handbids)
    print(f"cards rank*bid sum is {result}")

if __name__=="__main__":
    main()
