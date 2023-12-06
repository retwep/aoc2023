import sys

def get_digit(s:str):
    if s[0] in "0123456789":
        return int(s[0])
    return None
    names = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    for index,value in enumerate(names):
        if s.startswith(value):
            return index
    return None

def code(l:str):
    first = None
    last = None
    l = l.strip().lower()
    for i in range(0,len(l)):
        digit = get_digit(l[i:])
        if digit is not None:
            if first is None:
                first = digit
            last = digit
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
