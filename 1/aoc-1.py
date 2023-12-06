import sys

def get_digit(s:str):
    if s[0] in "0123456789":
        return int(s[0]),1
    # return None
    names = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    for index,value in enumerate(names):
        if s.startswith(value):
            return index, len(value)
    return None,1

def code(l:str):
    first = None
    last = None
    l = l.strip().lower()
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


def main():
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
