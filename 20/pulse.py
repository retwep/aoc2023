#!/usr/bin/env python
import sys
from typing import Any, Dict, List

class Node:
    """base class for all circuit blocks"""
    def __init__(self, name:str, outputs:List[str]):
        self.name = name
        self.out_names = outputs
        self.inputs:Dict[str, "Node"] = dict()
        self.outputs:Dict[str, "Node"] = dict()
        self.in_values:Dict[str, bool] = dict()
        self.sent_low: int = 0
        self.sent_high: int = 0

    def reset(self):
        self.sent_low: int = 0
        self.sent_high: int = 0
        for k in self.in_values.keys():
            self.in_values[k] = False

    def attach_outputs(self, all_nodes:Dict[str, "Node"]):
        for name in self.out_names:
            node = all_nodes.get(name)
            if node is None:
                # generic output sort of a node, something with no operation and no connections.
                node = Output(name, [])
                all_nodes[name] = node
            self.add_output(node)
            node.add_input(self) # don't need this?

    def count_pulse(self, pulse:bool):
        if pulse:
            self.sent_high +=1
        else:
            self.sent_low += 1

    def add_input(self, from_node:"Node"):
        self.inputs[from_node.name] = from_node
        self.in_values[from_node.name] = False
    
    def add_output(self, to_node:"Node"):
        self.outputs[to_node.name] = to_node

    def input_pulse(self, pulse:bool, node:"Node", backlog:List["Pulse"]) -> None:
        assert False, "process_pulse() must be implemented for each node type"


class Pulse:
    """closure for pulses to be sent in the future"""
    def __init__(self, pulse:bool, sender:Node, destination:Node, backlog:List["Pulse"]):
        self.pulse = pulse
        self.sender = sender
        self.destination = destination
        self.backlog = backlog

    def transmit(self):
        self.destination.input_pulse(self.pulse, self.sender, self.backlog)
        self.sender.count_pulse(self.pulse)

class Button(Node):
    def input_pulse(self, pulse:bool, node:"Node", backlog:List["Pulse"]) -> None:
        assert node is None, "button doesn't have an upstream sender"
        for _,out_node in self.outputs.items():
            action = Pulse(pulse=False, sender=self, destination=out_node, backlog=backlog)
            backlog.append(action)

class Broadcaster(Node):
    """There is a single broadcast module (named broadcaster). When it receives a pulse,
    it sends the same pulse to all of its destination modules."""

    def input_pulse(self, pulse:bool, node:"Node", backlog:List["Pulse"]) -> None:
        self.in_values[node.name] = pulse
        for _,out_node in self.outputs.items():
            action = Pulse(pulse=pulse, sender=self, destination=out_node, backlog=backlog)
            backlog.append(action)
    
class FlipFlop(Node):
    """aoc flipflop initially off, high pulse ignored, low pulse change output state
    Flip-flop modules (prefix %) are either on or off; they are initially off. If a
    flip-flop module receives a high pulse, it is ignored and nothing happens. However,
    if a flip-flop module receives a low pulse, it flips between on and off. If it was
    off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse."""
    def __init__(self, *args:Any, **kwargs:Dict[str,Any]):
        super().__init__(*args, **kwargs)
        self.previous = False
    
    def reset(self):
        super().reset()
        self.previous = False

    def input_pulse(self, pulse:bool, node:"Node", backlog:List["Pulse"]) -> None:
        self.in_values[node.name] = pulse
        if pulse:
            return  # instructions says it does nothing
        
        self.previous = not self.previous
        for _,out_node in self.outputs.items():
            action = Pulse(pulse=self.previous, sender=self, destination=out_node, backlog=backlog)
            backlog.append(action)

class Conjunction(Node):
    """Conjunction modules (prefix &) remember the type of the most recent pulse received
    from each of their connected input modules; they initially default to remembering a low
    pulse for each input. When a pulse is received, the conjunction module first updates its
    memory for that input. Then, if it remembers high pulses for all inputs, it sends a low
    pulse; otherwise, it sends a high pulse."""
    def input_pulse(self, pulse:bool, node:"Node", backlog:List["Pulse"]) -> None:
        self.in_values[node.name] = pulse
        output = True
        if all([x for x in self.in_values.values()]):
            output = False
        for _,out_node in self.outputs.items():
            action = Pulse(pulse=output, sender=self, destination=out_node, backlog=backlog)
            backlog.append(action)

class Output(Node):
    """The directions do not define output node, explain what it does or how it works.  Just implied that other nodes send it pulses."""
    def input_pulse(self, pulse:bool, node:"Node", backlog:List["Pulse"]) -> None:
        self.in_values[node.name] = pulse
        if self.name == "rx" and not pulse:
            Circuit.trip()
        return

class Circuit:
    def __init__(self):
        self.nodes:Dict[str, Node] = dict()

    def add_node(self, node:Node):
        self.nodes[node.name] = node
    
    def connect_nodes(self):
        # when we first load everything we have names but not references.
        # this ties the references through the circuit
        stupid = self.nodes.copy() # NOT a deep copy! need Node references
        for node in stupid.values():
            node.attach_outputs(self.nodes)

    def push_button_and_wait(self):
        backlog:List[Pulse] = list()
        self.nodes["button"].input_pulse(pulse=False, node=None, backlog=backlog) # type: ignore
        while backlog:
            action:Pulse = backlog.pop(0)
            action.transmit()

    def count_high_low_pulses(self, presses:int):
        secondary = False
        for i in range(presses):
            self.push_button_and_wait()
            if Circuit.tripped and not secondary:
                print(f"Tripped at push {i+1}")
                secondary = True
        low = 0
        high = 0
        for node in self.nodes.values():
            low += node.sent_low
            high += node.sent_high
        return low,high
    
    def reset(self):
        for node in self.nodes.values():
            node.reset()
        

    @staticmethod
    def trip():
        if not Circuit.tripped:
            print(f"rx tripped at button press {Circuit.yucky_global_circuit.nodes['button'].sent_low}")
            Circuit.tripped = True

    yucky_global_circuit:"Circuit" = None
    tripped = False

    @staticmethod
    def parse_lines(lines:List[str]):
        result = Circuit()
        node = Button("button", ["broadcaster"])
        result.add_node(node)

        for line in lines:
            n_str, o_str = line.split(" -> ")
            outputs = o_str.split(", ")
            if line[0] == "%":
                name = n_str[1:]
                node = FlipFlop(name=name, outputs=outputs) # type: ignore
            elif line[0] == "&":
                name = n_str[1:]
                node = Conjunction(name=name, outputs=outputs)
            else:
                name = n_str
                print(f"adding {name}")
                assert name == "broadcaster"
                node = Broadcaster(name=name, outputs=outputs)
            result.add_node(node)
        
        result.connect_nodes()
        Circuit.yucky_global_circuit = result
        return result


def test():
    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    lines = [r.strip() for r in raw_lines]

    circuit = Circuit.parse_lines(lines)

    low, high = circuit.count_high_low_pulses(1000)
    print(f"got {low=}, {high=}, product: {low*high}")

    circuit.reset()
    count = 0
    while not Circuit.tripped:
        count += 1
        circuit.push_button_and_wait()



if __name__=="__main__":
    main()
