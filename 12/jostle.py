#!/usr/bin/env python
import sys
from typing import Any, List, Tuple


def parse_spring_data(lines:List[str]) -> Tuple[List[str], List[List[int]]]:
    fixmes:List[str] = list()
    patterns:List[List[int]] = list()
    for line in lines:
        fm, pt = line.split()
        fixmes.append(f".{fm}?{fm}?{fm}?{fm}?{fm}.")
        patt:List[int] = [int(y) for y in pt.split(",")]
        pc = patt.copy()
        patt.extend(pc)
        patt.extend(pc)
        patt.extend(pc)
        patt.extend(pc)
        patterns.append(patt)
    return fixmes, patterns

def count_variations(fixme:str, pattern:List[int]) -> int:
    count:int = 0

    if len(pattern) == 0:
        assert len(fixme) == 0
        # we got to the end and didn't fail, so we must have succeeded
        return 0

    # at this level of recursion, what is the last position this pattern can occupy before we can't fit the rest of the pattern.
    # iterate from 0 to that last slot.
    #   apply quantity of # and separator . at position - does it create a valid match?
    #   if not, continue
    #   if so,
    #       trim the remaining fixme and pattern and recurse
    #       if None, assume failure of recursion
    #       if not None, sum the count
    return count

def test():
    
    cases = [(".???.###.", [1,1,3] ,1)]
             
    for case in cases:
        v = count_variations(case[0], case[1])
        print(f"{case=}, {v=}")
        assert v == case[2]

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    fixmes, patterns = parse_spring_data(lines)
    count:int = 0
    for fixme,pattern in zip(fixmes, patterns):
        count += count_variations(fixme, pattern)
    print(f"total variations {count}")


if __name__=="__main__":
    main()
