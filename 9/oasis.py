#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple

def diffs(values:List[int]) -> List[int]:
    assert len(values) > 1, f"Too few values to diff! {values=}"
    diff = list()
    for i in range(len(values)-1):
        diff.append(values[i+1]-values[i])
    return diff

def make_layer_diffs(values:List[int]) -> List[int]:
    layers = list()
    layers.append(values.copy())  # first layer is the input
    while True:
        next = diffs(layers[-1])
        layers.append(next)
        assert next
        if not any(next):
            break
    return layers


def interpolate(values:List[int]) -> List[int]:
    layers = make_layer_diffs(values)

    for i in range(1,len(layers)):
        new = layers[-i][-1] + layers[-(i+1)][-1]
        layers[-(i+1)].append(new)

    return layers[0]

def interpolate_back(values:List[int]) -> List[int]:
    layers = make_layer_diffs(values)

    for i in range(1,len(layers)):
        new = layers[-(i+1)][0] - layers[-i][0]
        layers[-(i+1)].insert(0,new)

    return layers[0]


def test():
    assert interpolate([1, 1]) == [1, 1, 1]
    assert interpolate([1, 2, 3]) == [1,2,3,4]
    assert interpolate([1,2,4,7]) == [1,2,4,7,11]

    assert interpolate_back([1, 1]) == [1, 1, 1]
    assert interpolate_back([1, 2, 3]) == [0,1,2,3]
    assert interpolate_back([1,2,4,7]) == [1,1,2,4,7]

    print("Test passed")

def parse_readings(lines: List[str]) -> List[List[int]]:
    all = list()
    for line in lines:
        readings = [int(v) for v in line.split(" ") if v != ""]
        assert len(readings) > 2, f"Too few readings!! {line=}\n{readings=}\n{lines=}\n"
        all.append(readings)
    return all

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]

    readings = parse_readings(lines)
    sum = 0
    backsum = 0
    for reading in readings:
        interpolated = interpolate(reading)
        if len(reading) < 10:
            print(f"{interpolated=}")
        sum += interpolated[-1]
        back = interpolate_back(reading)
        if len(reading) < 10:
            print(f"{back=}")
        backsum += back[0]

    print(f"Sum of interpolations {sum}")
    print(f"Sum of back interpolations {backsum}")



if __name__=="__main__":
    main()
