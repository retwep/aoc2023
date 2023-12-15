#!/usr/bin/env python
import regex
import sys
from typing import List, Tuple, Union

def parse_spring_data(lines:List[str]) -> Tuple[List[str], List[List[int]]]:
    fixmes:List[str] = list()
    patterns:List[List[int]] = list()
    for line in lines:
        fm, pt = line.split()
        rfm = f"{fm}?{fm}?{fm}?{fm}?{fm}"
        rfm = rfm.replace("..", ".")
        rfm = rfm.replace("..", ".")
        rfm = rfm.replace("..", ".")
        rfm = rfm.replace("..", ".")
        rfm = rfm.replace("..", ".")
        fixmes.append(rfm)
        patt:List[int] = [int(y) for y in pt.split(",")]
        pc = patt.copy()
        patt.extend(pc)
        patt.extend(pc)
        patt.extend(pc)
        patt.extend(pc)
        patterns.append(patt)
    return fixmes, patterns

def count_variations(fixme:str, pattern:List[int]) -> Union[int, None]:
    count:int = 0

    while fixme.startswith("."):
        fixme = fixme[1:]
    while fixme.endswith("."):
        fixme = fixme[0:-1]
    
    if fixme.startswith("?"):
        # look for an explict run of "?????###" in fixme that matches or exceeds the largest pattern
        mp = max(pattern)
        if  

    if len(pattern) == 0:
        if "#" in fixme:
            return None
        # we used all the pattern and have no # left unmatched, so we must have succeeded
        return 0

    # at this level of recursion, what is the last position this pattern can occupy before we can't fit the rest of the pattern.
    p = pattern[0]
    overlay = "#"*p + "."
    s = sum(pattern)+len(pattern)-1  # the amount of space we need for the remaining pattern and minimal separators
    maxlen = len(fixme) - s # the amount of unused space for child variants to expand into.
    i = 0
    while i <= maxlen: # iterate from 0 to that last slot.
        # apply quantity of # and separator . at position - does it create a valid match?
        for x in range(0,p):
            if fixme[x+i] == "#" and overlay[x] != "#":
                break
            if fixme[x+i] == "." and overlay[x] != ".":
                break

            # if fixme[x+i] == "?" # don't care what overlay is.
        else:
            # we didn't break, so we have a match!
            # trim the remaining fixme and pattern and recurse
            sub = count_variations(fixme[i+p+1:], pattern[1:])
            if sub is not None:
                # valid matches
                count += sub+1
        i += 1
    if count == 0:
        # found no valid configurations
        return None
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
        result:Union[int, None] = count_variations(fixme, pattern)
        assert result is not None, "We didn't find any count! this is a bug!"
        count += result
    print(f"total variations {count}")


if __name__=="__main__":
    main()
