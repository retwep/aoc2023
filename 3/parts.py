import sys

def get_digit(s:str):
    if s[0] in "0123456789":
        return int(s[0]),1
    return None,1  # without see below, with 54338
    names = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    for index,value in enumerate(names):
        if s.startswith(value):
            return index, 1  # len(value)  # 1 == 53389, len == 53407
    return None,1

def code(l:str):
    first = None
    last = None
    l = l.strip().lower()
    # these 2 are in input.txt
    # assert "twone" not in l
    # assert "oneight" not in l
    """ these are not in input.txt but trip the test cases
    assert "zerone" not in l
    assert "threeight" not in l
    assert "nineight" not in l
    """
    i = 0
    while i < len(l):
        digit,skip = get_digit(l[i:])
        i += skip
        if digit is not None:
            if first is None:
                first = digit
            last = digit
    assert first is not None
    result = 10*first+last

    print(f"line:  {l}  {first=}, {last=}, {result=}")
    return result

def test():
    assert code("0") == 0
    assert code("1") == 11
    assert code("2") == 22
    assert code("3") == 33
    assert code("4") == 44
    assert code("5") == 55
    assert code("6") == 66
    assert code("7") == 77
    assert code("8") == 88
    assert code("9") == 99
    assert code("zero") == 0
    assert code("one") == 11
    assert code("two") == 22
    assert code("three") == 33
    assert code("four") == 44
    assert code("five") == 55
    assert code("six") == 66
    assert code("seven") == 77
    assert code("eight") == 88
    assert code("nine") == 99

    assert code("01") == 1
    assert code("12") == 12
    assert code("123") == 13
    assert code("a1b") == 11
    assert code("a1b2") == 12
    assert code("3a1b2") == 32

    assert code("four1five") == 45
    assert code("1six8") == 18
    assert code("onetwo") == 12
    assert code("nineight") == 98
    assert code("nineeight") == 98
    assert code("twone") == 21
    assert code("twoone") == 21
    assert code("oneabd") == 11
    assert code("zxzeroneabd") == 1
    assert code("zxzerooneabd") == 1


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw = f.readlines()
    sum = 0
    for line in raw:
        value = code(line)
        sum += value
    print(f"{sum=}")

if __name__=="__main__":
    main()
