#!/usr/bin/env python

# submission 3: 528819 was correct for part 1
# submission 2: gives 529964 and web page says it is too high.
# submission 1: previously got 332309 and web page says it was too low.

import sys
from typing import List, Tuple

digits = "0123456789"

def check_symbol(x:str) -> str:
    for c in x:
        if c not in digits and c != ".":
            return c
    return ''

class Symbol:
    def __init__(self, matrix:List[str], row:int, col:int, c:str):
        self.matrix = matrix
        self.row = row
        self.col = col
        self.symbol = c
        self.numbers:List["PartNumber"] = list()
        self.key = f"{row}x{col}"  # need this or not?

    def is_gear(self):
        return self.symbol == "*" and len(self.numbers) == 2
    
    def gear_power(self):
        if not self.is_gear():
            return None
        return self.numbers[0].value * self.numbers[1].value

    def add_number(self, number:"PartNumber"):
        self.numbers.append(number)
    
class PartNumber:
    def __init__(self, matrix:List[str], row:int, col:int, width:int):
        self.matrix = matrix
        self.row = row
        self.col = col
        self.width = width
        self.symbols:List[Symbol] = list()
        self.value = int(matrix[row][col:col+width])
        self.key = f"{row}x{col}"  # leftmost digit
    
    def is_part(self):
        return any(self.symbols)

    def scan_around_for_symbols(self, symbols):
        left = self.col - 1
        right = self.col + self.width
        def generate_symbol(m:List[str], row:int, col:int):
            nonlocal self
            s = check_symbol(m[row][col])
            if s:
                symbol = Symbol(m, row, col, s)
                self.symbols.append(symbol)
                symbol.add_number(self)
                return symbol
            return None

        # row above
        for c in range(left, right+1):
            generate_symbol(self.matrix, self.row-1, c)

        # left/right
        generate_symbol(self.matrix, self.row, left)
        generate_symbol(self.matrix, self.row, right)

        # row below
        for c in range(left, right+1):
            generate_symbol(self.matrix, self.row+1, c)


    @staticmethod
    def parse_number(matrix:List[str], row:int, col:int, numbers:List["PartNumber"], symbols:List[Symbol]) -> int:
        width = 1
        while matrix[row][col+width] in digits:
            width += 1
        number = PartNumber(matrix, row, col, width)
        numbers.append(number)

        number.scan_around_for_symbols(symbols)
        return width

def scan_the_matrix(matrix:List[str]) -> Tuple[List[PartNumber], List[Symbol]]:
    part_numbers = list()
    symbols = list()

    lm0 = len(matrix[0])
    row = 0
    while row < len(matrix) - 1: # reduced because matrix was padded and we don't need to scan bottom line
        col = 1 # skip padding
        while col < lm0 - 1:
            c = matrix[row][col]
            if c in digits:
                advance = PartNumber.parse_number(matrix, row, col, part_numbers, symbols)
            else:
                advance = 1
            col += advance
        row += 1
    return (part_numbers, symbols)

def pad_the_matrix(matrix:List[str]) -> List[str]:
    # pad it once then ignore all boundary conditions. Yay Lazy.
    lm0 = len(matrix[0])+2
    blank = "." * lm0

    padded = [blank]
    for l in matrix:
        padded.append(f".{l}.")
    padded.append(blank)
    return padded

def test():
    padded = pad_the_matrix(["x"])
    assert padded == ["...", ".x.", "..."]

    def check_part_numbers(raw:List[str], expected:List[int]):
        print(raw)
        matrix = pad_the_matrix(raw)
        pn, s = scan_the_matrix(matrix)
        parts = sorted([p.value for p in pn if p.is_part()])
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
        parts = check_part_numbers(i[0], i[1])
        swapped = [i[0][1], i[0][0]]
        parts = check_part_numbers(swapped, i[1])

    # above, below, diagonal
    inputs = [(
        ["123...456",
         "^789.*222",
         "123...123"], [123,123,123,222,456,789])
    ]
    for i in inputs:
        check_part_numbers(i[0], i[1])

    # check for only single count if only single part
    for i in range(0,9):
        x = list("."*9)
        x[i] = "#"
        x[4] = "7"
        matrix = ["".join(x[0:3]),"".join(x[3:6]),"".join(x[6:9])]
        expected = [] if i == 4 else [7]
        check_part_numbers(matrix, expected)

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    unpadded = [r.strip() for r in raw_lines]
    schematic = pad_the_matrix(unpadded)
    numbers, symbols = scan_the_matrix(schematic)
    parts = sorted([p.value for p in numbers if p.is_part()])
    part_sum = sum(parts)
    print(f"{part_sum=}")
    gears = [s for s in symbols if s.is_gear()]
    

if __name__=="__main__":
    main()
