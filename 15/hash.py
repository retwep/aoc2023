#!/usr/bin/env python
import sys
from typing import Dict, List, Union

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

class Lens:
    def __init__(self, label:str, focal:int):
        self.box:int = hash(label)
        self.label:str = label
        self.focal:int = focal
        
class Box:
    def __init__(self, hash:int):
        self.lenses:List[Lens] = list()
        self.hash:int = hash

    def set_lens(self, lens:Lens):
        for l in self.lenses:
            if l.label == lens.label:
                l.focal = lens.focal
                break
        else:
            self.lenses.append(lens)

    def remove_lens(self, label:str):
        for l in self.lenses:
            if l.label == label:
                self.lenses.remove(l)
    
    def lens_score(self) -> int:
        pf=0
        for l, lens in enumerate(self.lenses):
            pf += (1+self.hash) * (l+1) * lens.focal
        return pf
        
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

def configure_lens_boxes(directions:str) -> int:
    steps:List[str] = directions.split(",")
    boxes:Dict[int,Box] = dict()
    for step in steps:

        if "=" in step:
            label, fs = step.split("=")
            boxid =  hash(label)
            if not (b := boxes.get(boxid)):
                b = Box(boxid)
                boxes[boxid] = b
            
            focal = int(fs)
            l = Lens(label, focal)
            b.set_lens(l)

        elif "-" in step:
            label = step[0:-1]
            assert "-" not in label, f"Assert - not in {label=}"
            boxid =  hash(label)
            if not (b := boxes.get(boxid)):
                b = Box(boxid)
                boxes[boxid] = b
            b.remove_lens(label)
    total = 0
    for box in boxes.values():
        total += box.lens_score()
    return total


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    directions = "".join([r.strip() for r in raw_lines])
    part1 = hash_all(directions)
    print(f"{part1=}")

    value = configure_lens_boxes(directions)
    print(f"part2 = {value}")

if __name__=="__main__":
    main()
