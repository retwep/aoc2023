#!/usr/bin/env python

# This gives 529964 and web page says it is too high.
# previously got 332309 and web page says it was too low.

import sys
from typing import List, Set

digits = "0123456789"

def check_symbol(x):
    for c in x:
        if c not in digits and c != ".":
            return True
    return False

def scan_parts(a, b, c) -> List:
    above = f".{a}." # very lazy edges
    here = f".{b}." # very lazy edges
    below = f".{c}." # very lazy edges
    parts = list()
    number = ""
    is_part = False
    for i,c in enumerate(here):
        if c in digits:
            number = number+c # may or may not be a part number
            is_part |= check_symbol([above[i-1], above[i], above[i+1], here[i-1], here[i+1], below[i-1], below[i], below[i+1]])
        else:
            if number:
                if is_part:
                    if int(number) in parts:
                        print(f"A multi-part {number}")
                    parts.append(int(number))
                number = ""
                is_part = False
    if number:
        if is_part:
            if int(number) in parts:
                print(f"B multi-part {number}")
            parts.append(int(number))
    return parts


def part_numbers(matrix) -> List:
    parts = list()
    blank = "." * len(matrix[0])
    for i, line in enumerate(matrix):
        assert len(line) == len(matrix[0])
        found = scan_parts(blank if i == 0 else matrix[i-1], line, blank if i+1 == len(matrix) else matrix[i+1])
        parts.extend(found)
    return sorted(parts)


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
    check_part_numbers([".#123$"], [123])  # ambiguity here -- is this 1 part number or 2? let's try to catch it
    check_part_numbers([".#123$123."], [123, 123])
    check_part_numbers([".#123..$123."], [123, 123])
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
        assert parts == i[1], f"(swapped) {swapped=}  found {parts}, expected {i[1]}"

    # above, below, diagonal
    inputs = [(
        ["123...456",
         "^789.*222",
         "123...123"], [123,123,123,222,456,789])
    ]
    for i in inputs:
        parts = part_numbers(i[0])
        assert parts == i[1], f"found {parts}, expected {i[1]}"

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
