#!/usr/bin/env python
import copy
import sys
from typing import List, Union

def parse_patterns(lines:List[str]) -> List[List[List[str]]]:
    patterns:List[List[List[str]]] = list()
    s=0
    for i, line in enumerate(lines):
        if not line:
            patterns.append([[c for c in l] for l in lines[s:i]])
            s=i+1
    patterns.append([[c for c in l] for l in lines[s:]])
    return patterns

def is_mirror(line:List[str], i:int) -> bool:
    x = 1
    if i+1 >= len(line):
        return False
    while i-x+1 >= 0 and i+x < len(line):
        if line[i-x+1] != line[i+x]:
            return False
        x += 1
    return True

def find_all_mirrors(line:List[str]) -> Union[List[int],None]:
    mirrors:List[int] = list()
    for i in range(0,len(line)):
        # assume the mirror line here and check for reflection
        m = is_mirror(line, i)
        if m:
            mirrors.append(i)
    if not mirrors:
        return None
    return mirrors
        
def find_vertical_mirror(pattern:List[List[str]], exclude:Union[int,None] = None) -> Union[int, None]:
    found:List[int] = list()
    mirrors:Union[List[int],None] = find_all_mirrors(pattern[0])
    if not mirrors:
        return None
    for m in mirrors:
        for row in pattern[1:]:
            if not is_mirror(row, m):
                break
        else:
            if m != exclude:
                found.append(m)
                assert len(found) == 1, f"too many mirrors? {pattern}, {found=}"
    if found:
        assert len(found) == 1, f"too many matches??? {pattern=}, {found=}"
        return found[0]
    return None
    
def transpose(pattern:List[List[str]]) -> List[List[str]]:
    pt:List[List[str]] = list()
    for i in range(0,len(pattern[0])):
        t:List[str]=list()
        for j in range(0,len(pattern)):
            t.append(pattern[j][i])
        pt.append(t)
    return pt

def test():
    def ml(x:str)->List[str]:
        return [c for c in x]
    assert is_mirror(ml("xx"),0)
    assert not is_mirror(ml("XxxX"),0)
    assert is_mirror(ml("XxxX"),1)
    assert not is_mirror(ml("XxxX"),2)
    assert not is_mirror(ml("XxxX"),3)
    a = find_all_mirrors(ml("AXxxX"))
    assert a
    assert a[0] == 2 and len(a) == 1, f"{a=}"
    a = find_all_mirrors(ml("XXxxX"))
    assert a
    assert a[0] == 0 and a[1] == 2 and len(a) == 2, f"{a=}"

    print("Test passed")


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    patterns:List[List[List[str]]] = parse_patterns(lines)
    vertical:int = 0
    horizontal:int = 0
    for pattern in patterns:
        smudge_found = False
        sx = find_vertical_mirror(pattern)
        tpatt:List[List[str]] = transpose(pattern)
        sy = find_vertical_mirror(tpatt)
        for col in range(0,len(pattern[0])):
            for row in range(0,len(pattern)):
                cleaned:List[List[str]] = copy.deepcopy(pattern)
                cleaned[row][col] = "." if cleaned[row][col] == "#" else "#"
                x = find_vertical_mirror(cleaned, sx)
                if x is not None and sx != x:
                    vertical += x+1
                    smudge_found = True
                tpatt:List[List[str]] = transpose(cleaned)
                y = find_vertical_mirror(tpatt, sy)
                if y is not None and sy != y:
                    horizontal += y+1
                    smudge_found = True
                if smudge_found:
                    break
            if smudge_found:
                break
                
    print(f"{vertical=}, {horizontal=}, summary={vertical+100*horizontal}")


if __name__=="__main__":
    main()
