#!/usr/bin/env python
from box import Box
import sys
from typing import Dict, List, Tuple, Union

class Part:
    def __init__(self, x:int, m:int, a:int, s:int):
        self.b = Box()
        self.b["x"] = x
        self.b["m"] = m
        self.b["a"] = a
        self.b["s"] = s
    
    def score(self) -> int:
        b:Box = self.b
        return b.x+b.m+b.a+b.s

    @staticmethod
    def parse(raw:str) -> "Part":
        r2 = raw.replace("{", "").replace("}", "")
        r3 = r2.split(",")
        k:Dict[str,int] = dict()
        for v in r3:
            n,val = v.split("=")
            k[n] = int(val)
        return Part(**k)


class Rule:
    def __init__(self, field:Union[None,str], operator:Union[None,str], value:Union[None,int], next:str):
        self.field = field
        self.operator:Union[None,str] = operator
        self.value:Union[None,int] = value
        self.next:str = next

    def evaluate(self, part:Part) -> str:
        if self.operator is None:
            return self.next
        elif self.operator == ">":
            if part.b[self.field] > self.value:
                return self.next
        elif self.operator == "<":
            if part.b[self.field] < self.value:
                return self.next
        return ""  # blank means keep trying other rules, no match
    
    @staticmethod
    def build_rule(raw:str) -> "Rule":
        field = None
        operator = None
        value = None
        next = None
        if ":" in raw:
            expr, next = raw.split(":")
            if ">" in expr:
                field, vstr = expr.split(">")
                operator = ">"
            else:
                assert "<" in expr
                field, vstr = expr.split("<")
                operator = "<"
            if vstr:
                value = int(vstr)
        else:
            next = raw
        return Rule(field, operator, value, next)

class Flow:
    def __init__(self, name:str, rules:str):
        self.name = name
        assert len(name) >= 2, "must have 2 digit names at least so that A and R will work"
        self.rule_str = rules.replace("{", "").replace("}", "")
        self.rules:List[Rule] = self.split_rules()
    
    def split_rules(self) -> List[Rule]:
        rules:List[Rule] = list()
        raw = self.rule_str.split(",")
        for rstr in raw:
            rule:Rule = Rule.build_rule(rstr)
            rules.append(rule)
        return rules

        
    def process_flow(self, part:Part) -> str:
        for rule in self.rules:
            result = rule.evaluate(part)
            if result:
                return result
        assert False, f"{part=} failed to match {self.name} "

def find_flow(fd:Dict[str, Flow], flows:List[Flow], name:str) -> Flow:
    # yeah, sure, we could do this as a pure dictionary. whatevs
    if name in fd:
        return fd[name]
    for flow in flows:
        if flow.name == name:
            fd[name] = flow
            return flow
    assert False, f"No match? {name=}"
    return Flow("", "")


def factory(flows:List[Flow], parts:List[Part]) -> List[Part]:
    accepted:List[Part] = list()
    next = "in"
    fd:Dict[str, Flow] = dict()
    while parts:
        part = parts[0]
        flow = find_flow(fd, flows, next)
        next = flow.process_flow(part)
        if next == "A":
            accepted.append(part)
            parts.pop(0)
            next = "in"
        elif next == "R":
            parts.pop(0)
            next = "in"
    
    return accepted

def test():
    tests:List[Tuple[Flow, Part, str]] = [
        (Flow("abc1", "{a<1:def,x>1:ghi,m>1:A,R}"), Part(x=1,m=2,a=3,s=4), "A"),
        (Flow("abc2", "{a>1:def,x<1:ghi,m<1:A,R}"), Part(x=1,m=2,a=1,s=4), "R"),
        (Flow("abc3", "{a<1:def,x>1:ghi,m>1:A,R}"), Part(x=1,m=2,a=0,s=4), "def"),
        (Flow("abc4", "{a>1:def,x<1:ghi,m<1:A,R}"), Part(x=0,m=2,a=1,s=4), "ghi")
    ]

    for test in tests:
        f = test[0]
        p = test[1]
        expected = test[2]
        result = f.process_flow(p)
        assert result == expected, f"flow {f.name} failed {expected=}, {result=}"
    print("Test passed")

def parse_lines(lines:List[str]) -> Tuple[List[Flow], List[Part]]:
    flows:List[Flow] = list()
    parts:List[Part] = list()
    for line in lines:
        if not line:
            continue
        if "=" in line:
            part = Part.parse(line)
            parts.append(part)
        else:
            n, f = line.split("{")
            f = f[0:-1]
            flow = Flow(n, f)
            flows.append(flow)

    return flows, parts


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]
    flows, parts = parse_lines(lines)
    accepted = factory(flows, parts)
    total = 0
    for part in accepted:
        total += part.score()
    
    print(f"score: {total},  {len(accepted)=}")
    

if __name__=="__main__":
    main()
