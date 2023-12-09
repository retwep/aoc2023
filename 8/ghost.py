#!/usr/bin/env python

# part1 submission 1 12083

from sympy import primefactors
import sys
from typing import Dict, List, Set, Tuple

def navigate(turns:str, map:Dict[str,Dict[str,str]], forced = None) -> int:
    ghosts = [key for key in map.keys() if key.endswith("A")]
    if forced:
        ghosts = forced

    print(f"There are {len(ghosts)} : {ghosts=}")

    tm = len(turns)
    lengths = list()

    # get the path length for each ghost's individual path
    for g in ghosts:
        ghost = g
        count = 0
        while not ghost.endswith("Z"):
            turn = turns[count % tm]
            count += 1
            ghost = map[ghost][turn]
        print(f"Ghost {g} path length is {count}")
        lengths.append(count)
    
    # get prime factors for each path length
    primes = list()
    for i, l in enumerate(lengths):
        p = primefactors(l)
        print(f"ghost {ghosts[i]} has prime factors {p}")
        primes.extend(primefactors(l))
    
    # dear reader, why is this done this way one at a time when the puzzle said at the same time?
    # because it ends up being a modulo math problem where you have to wait for all of the paths
    # to repeat at their own frequency until they all come up even.  This will happen at a number of
    # repeats of the multiple of all prime factors of each.
    # How many times must you iterate 3 and 5 before they both have a common multiple:
    # [3]  [5]
    #  1    1    
    #  2    2
    #  3Z   3
    #  1    4
    #  2    5Z
    #  3Z   1
    #  1    2
    #  2    3
    #  3Z   4
    #  1    5Z
    #  2    1
    #  3Z   2
    #  1    3
    #  2    4
    #  3Z   5Z

    # maybe not correct for general case but works for this one:
    primes = set(primes)
    
    # result is the product
    def product(p: Set):
        prod = 1
        for i in p:
            prod *= i
        return prod
    
    return product(primes)


def load_map(lines:List[str]) -> Tuple[str,Dict[str,Dict[str,str]]]:
    directions = lines[0]
    map = dict()
    for line in lines[2:]:
        line = line.replace(" ", "")
        key, t = line.split('=')
        t = t.split(',')
        left = t[0][1:]
        right = t[1].strip()[:-1]
        assert key not in map
        map[key] = {"L":left,"R":right}
    print(f"Map has {len(directions)} turns and {len(map)} keys")
    return directions, map

def test():
    d,m = load_map(["L", "", "AAA = (ZZZ,AAA)"])
    assert d == "L"
    assert m == {"AAA": {"L": "ZZZ", "R":"AAA"}}

    turns = navigate(d, m)
    assert turns == 1
    d = "LLR"
    m = {"AAA": {"L":"B", "R":"Z"},
         "B": {"L":"C", "R":"Z"},
         "C": {"L":"Z", "R":"D"},
         "D": {"L":"E", "R":"Z"},
         "E": {"L":"F", "R":"Z"},
         "F": {"L":"Z", "R":"ZZZ"},
         "Z": {"L":"Z", "R":"Z"},
         }
    turns = navigate(d,m)
    assert turns == 6

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    d,m = load_map(lines)

    """
    # ok, here's a major spoiler -- it was taking so long to finish that I started looking at what I can learn.
    # path length in single terms for each of the ghosts
    print(f"{navigate(d,m,['AAA'])}")
    print(f"{navigate(d,m,['FXA'])}")
    print(f"{navigate(d,m,['KNA'])}")
    print(f"{navigate(d,m,['QXA'])}")
    print(f"{navigate(d,m,['JVA'])}")
    print(f"{navigate(d,m,['FSA'])}")

    # path length in pairwise terms for each of the ghosts
    print(f"{navigate(d,m,['AAA','FXA'])}")
    print(f"{navigate(d,m,['FXA','KNA'])}")
    print(f"{navigate(d,m,['KNA','QXA'])}")
    print(f"{navigate(d,m,['QXA','JVA'])}")
    print(f"{navigate(d,m,['JVA','FSA'])}")
    print(f"{navigate(d,m,['FSA','AAA'])}")
    
    # path length in triples terms for each of the ghosts
    print(f"{navigate(d,m,['AAA','FXA','KNA'])}")
    print(f"{navigate(d,m,['FXA','KNA','QXA'])}")
    print(f"{navigate(d,m,['KNA','QXA','JVA'])}")
    print(f"{navigate(d,m,['QXA','JVA','FSA'])}")
    print(f"{navigate(d,m,['JVA','FSA','AAA'])}")
    print(f"{navigate(d,m,['FSA','AAA','FXA'])}")

    # by this point you should realize there is an analytical solution -- figure out the
    # unique factors of the single path length, then multiply them together from each of the ghosts
    # I didn't code that part, but got 
    # 1, 43, 281, 12083
    # 1, 47, 281, 13207
    # 1, 79, 281, 22199
    # 1, 61, 281, 17141
    # 1, 67, 281, 18827
    # 1, 73, 281, 20513
    #
    # which if you multiply the prime factors together you get:
    print("The analytical answer is ", 43*47*79*61*67*73*281)
    # of course this was by hand and not by program, does that count?
    """

    turns = navigate(d,m)
    print(f"map took {turns=}")

if __name__=="__main__":
    main()
