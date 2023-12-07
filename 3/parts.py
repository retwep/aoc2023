#!/usr/bin/env python

# This gives 332309 and web page says it is too low.

import sys
from typing import List, Set

digits = "0123456789"

def check_symbol(x):
    for c in x:
        if c not in digits and c != ".":
            return True
    return False

def simple_scan(raw1, raw2) -> Set:
    line1 = f".{raw1}." # very lazy edges
    line2 = f".{raw2}."
    parts = set()
    number = ""
    is_part = False
    for i,c in enumerate(line1):
        if c in digits:
            number = number+c # may or may not be a part number
            is_part |= check_symbol([line1[i-1], line1[i+1], line2[i-1], line2[i], line2[i+1]])
        else:
            if number:
                if is_part:
                    if int(number) in parts:
                        print(f"A multi-part {number}")
                    parts.add(int(number))
                number = ""
                is_part = False
    if number:
        if is_part:
            if int(number) in parts:
                print(f"B multi-part {number}")
            parts.add(int(number))
    return parts


def scan_parts(line1, line2) -> Set:
    found = simple_scan(line1, line2)
    f2 = simple_scan(line2, line1)
    if found.intersection(f2):
        print(f"APart intersection {found}, {f2}")
    return found.union(f2)

def part_numbers(matrix) -> List:
    parts = set()
    blank = "." * len(matrix[0])
    for i, line in enumerate(matrix):
        assert len(line) == len(matrix[0])
        found = scan_parts(line, matrix[i+1] if i+1 < len(matrix) else blank)
        if parts.intersection(found):
            print(f"duplicate part {parts.intersection(found)}")
        parts = parts.union(found)  # assumes part number 123 is only counted once no matter how many times it shows in the schematic
    return sorted(list(parts))


def test():
    def check_part_numbers(raw, expected):
        print(raw)
        parts = part_numbers(raw)
        assert parts == expected, f"{raw=}  {parts} != {expected}"

    # single line
    check_part_numbers(["123"], [])
    check_part_numbers([".123."], [])
    check_part_numbers([".123"], [])
    check_part_numbers(["123."], [])
    check_part_numbers([".123!."], [123])
    check_part_numbers([".#123"], [123])
    check_part_numbers([".#123$"], [123])
    check_part_numbers([".#123$123."], [123])
    check_part_numbers([".#123..$123."], [123])
    check_part_numbers(["123#456"], [123,456])
    check_part_numbers(["123#%456.345"], [123,456])
    check_part_numbers(["325.123#%456.345"], [123,456])

    # above, below, diagonal
    inputs = [(
        ["123...456",
         "^........"], [123]),
        (["123...456",
          ".^......."], [123]),
        (["123...456",
          "..^......"], [123]),
        (["123...456",
          "...^....."], [123]),
        (["123...456",
          "....^...."], []),
        (["123...456",
          ".....^..."], [456]),
        (["123...456",
          "......$.."], [456]),
    ]
    for i in inputs:
        parts = part_numbers(i[0])
        assert parts == i[1], f"found {parts}, expected {i[1]}"
        swapped = [i[0][1], i[0][0]]
        parts = part_numbers(swapped)
        assert parts == i[1], f"(swapped) found {parts}, expected {i[1]}"

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        schematic = f.readlines()
    parts = part_numbers(schematic)
    part_sum = sum(parts)
    print(f"{part_sum=}")

if __name__=="__main__":
    main()
