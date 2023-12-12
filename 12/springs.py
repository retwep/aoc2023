#!/usr/bin/env python
import re
import sys
from typing import Any, List, Tuple


def build_unknown_map(line: str) -> Tuple[int, List[int]]:
    map:List[int] = list()
    count = 0
    for i, c in enumerate(line):
        if c == "?":
            map.append(i)
            count += 1
    return count, map


def build_regex(pattern:List[int]) -> Any:
    r = ["S*"]
    for n in pattern:
        r.append(f"X{{{n}}}")
    r.append("S*")
    rstr = "S+".join(r)
    reg = re.compile(rstr)
    return reg

def valid_variation(fixme:str, pattern:List[int]) -> bool:
    safe = fixme.replace('.','S').replace('#','X').replace('?','Q') # regex specials
    reg = build_regex(pattern)
    found = bool(reg.fullmatch(safe))
    return found

def parse_spring_data(lines:List[str]) -> Tuple[List[str], List[List[int]]]:
    fixmes:List[str] = list()
    patterns:List[List[int]] = list()
    for line in lines:
        fm, pt = line.split()
        fixmes.append(f".{fm}.")
        patt:List[int] = [int(y) for y in pt.split(",")]
        patterns.append(patt)
    return fixmes, patterns

def count_variations(fixme:str, pattern:List[int]) -> int:
    count:int = 0 
    bit_count, map = build_unknown_map(fixme)
    safe = fixme.replace('.','S').replace('#','X').replace('?','Q') # regex specials
    reg = build_regex(pattern)
    # brute force - try every possible arrangement (this is way too big, but whaterver)
    for potential in range(0,pow(2,bit_count)):
        bits = f"{potential:0>32b}"[-bit_count:]
        cl = [c for c in safe]
        for i, c in enumerate(bits):
            cl[map[i]] = "S" if c=="0" else "X"
        candidate = "".join(cl)
        if reg.fullmatch(candidate):
            count += 1
    return count

def test():
    assert valid_variation(fixme=".###.", pattern=[3])
    assert valid_variation(fixme=".#.#.", pattern=[1,1])
    assert not valid_variation(fixme=".#.", pattern=[3])
    assert not valid_variation(fixme=".##.", pattern=[1,1])
    
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
