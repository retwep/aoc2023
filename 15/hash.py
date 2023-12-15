#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple

def hash(s:str) -> int:
    cv = 0
    for c in s:
        o = ord(c)
        cv = cv + o
        cv = cv * 17
        cv = cv % 256
    return cv

def hash_all(s:str) -> int:
    many = s.split(",")
    sum = 0
    for m in many:
        sum += hash(m)
    return sum



def test():
    assert hash("H") == 200
    assert hash("rn=1") == 30
    assert hash("cm-") == 253
    assert hash("qp=3") == 97
    assert hash("cm=2") == 47
    assert hash("qp-") == 14
    assert hash("pc=4") == 180
    assert hash("ot=9") == 9
    assert hash("ab=5") == 197
    assert hash("pc-") == 48
    assert hash("pc=6") == 214
    assert hash("ot=7") == 231

    demo="rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    h = hash_all(demo)
    assert h == 1320
    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    part1 = hash_all("".join(lines))
    print(f"{part1=}")

if __name__=="__main__":
    main()
