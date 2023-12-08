#!/usr/bin/env python

# submission 3: 528819 was correct for part 1
# submission 2: gives 529964 and web page says it is too high.
# submission 1: previously got 332309 and web page says it was too low.

import sys
from typing import List, Set

digits = "0123456789"

def check_symbol(x):
    for c in x:
        if c not in digits and c != ".":
            return c
    return ''

def check_gear(tl,tc,tr, l, r, bl, bc, br):
    # This identifies a gear, but doesn't give the numbers.
    # need a solution that gives the numbers associated with a gear.
    # Refactor to full OO with x/y coords and gear<-->partnumber references?
    # or scan adjacent for part numbers and accumulate them?

    def zero_or_one_or_two(a,b,c):
        if b in digits:
            #  12.  .23  123
            return 1
        if a in digits and c in digits:
            # 1.3
            return 2
        if a in digits or b in digits or c in digits:
            # 1..  .2.  ..3
            return 1
        # ...
        return 0 
    count = zero_or_one_or_two(tl, tc, tr)
    count += zero_or_one_or_two(bl, bc, br)
    count += 1 if l in digits else 0
    count += 1 if r in digits else 0
    if count == 2:
        return True # this is a gear, but what about the part numbers?
    return False
        

def scan_parts(a, b, c) -> List:
    above = f".{a}." # very lazy edges
    here = f".{b}." # very lazy edges
    below = f".{c}." # very lazy edges
    parts = list()
    number = ""
    is_part = False
    symbols = set()
    for i,c in enumerate(here): 
        if c == "*":
            if check_gear(above[i-1], above[i], above[i+1], here[i-1], here[i+1], below[i-1], below[i], below[i+1]):
                print(f"Found a gear! What do we do about it?\n{above}\n{here}\n{below}")

        if c in digits:
            number = number+c # may or may not be a part number
            cs = check_symbol([above[i-1], above[i], above[i+1], here[i-1], here[i+1], below[i-1], below[i], below[i+1]])
            is_part |= bool(cs)
            if cs:
                symbols.add(cs) # something weird going on - look for numbers with more than one symbol (not a perfect check, but simple to start)
        else:
            if number:
                if is_part:
                    if len(symbols) > 1:
                        print(f"Multi-symbol: {symbols=}")
                    if int(number) in parts:
                        print(f"A multi-part {number}")
                    parts.append(int(number))
                symbols = set()
                number = ""
                is_part = False
    if number:
        if is_part:
            if len(symbols) > 1:
                print(f"Multi-symbol: {symbols=}")
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

    # check for only single count if only single part
    for i in range(0,9):
        x = list("."*9)
        x[i] = "#"
        x[4] = "7"
        matrix = ["".join(x[0:3]),"".join(x[3:6]),"".join(x[6:9])]
        parts = part_numbers(matrix)
        expected = [] if i == 4 else [7]
        if parts != expected:
            print(f"FAIL: {matrix=}, {parts=}, {expected=}")
            assert False

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    schematic = [r.strip() for r in raw_lines]
    parts = part_numbers(schematic)
    part_sum = sum(parts)
    print(f"{part_sum=}")

if __name__=="__main__":
    main()
