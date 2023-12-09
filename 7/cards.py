#!/usr/bin/env python
import sys
from typing import Dict, List, Tuple

# comparable values for the kind of hand - why these values? :shrug:
FIVE_OF_A_KIND = 100
FOUR_OF_A_KIND = 75
FULL_HOUSE = 60
THREE_OF_A_KIND = 50
TWO_PAIR = 40
PAIR = 20
HIGHCARD = 10

class Hand:
    def __init__(self, cards:str, bid: int):
        self.cards = cards
        self.bid = bid
        self.category = self.rating()

    @staticmethod
    def card_value(c) -> int:
        values = "23456789TJQKA"
        assert c in values
        return values.find(c)

    def rating(self):
        d = dict()
        for card in self.cards:
            if d.get(card) is None:
                d[card] = 1
            else:
                d[card] += 1

        if len(d) == 1:
            # 5 of a kind
            return FIVE_OF_A_KIND
        if len(d) == 2:
            # four or fullhouse
            if d[self.cards[0]] in [3,2]:
                return FULL_HOUSE
            return FOUR_OF_A_KIND
        if len(d) == 3:
            # 2p or 3
            for k,v in d.items():
                if v == 1:
                    continue
                if v == 2:
                    return TWO_PAIR
                assert v == 3
                return THREE_OF_A_KIND
        if len(d) == 4:
            return PAIR
        assert len(d) == 5
        return HIGHCARD

    def __lt__(self, x:"Hand"):
        if self.category < x.category:
            return True
        if self.category > x.category:
            return False
        for a,b in zip(list(self.cards), list(x.cards)):
            if self.card_value(a) < self.card_value(b):
                return True
            elif self.card_value(a) > self.card_value(b):
                return False
        return False # equal
    def __gt__(self, x:"Hand"):
        if self.category > x.category:
            return True
        if self.category < x.category:
            return False
        for a,b in zip(list(self.cards), list(x.cards)):
            if self.card_value(a) > self.card_value(b):
                return True
            elif self.card_value(a) < self.card_value(b):
                return False
        return False # equal
    def __eq__(self, x):
        if self.category != x.category:
            return False
        for a,b in zip(list(self.cards), list(x.cards)):
            if self.card_value(a) != self.card_value(b):
                return False
        return True # equal
    
    def stronger_hand(self, b):
        if self < b:
            return -1
        if b < self:
            return 1
        return 0

def play_cards(hands):
    pass

def parse_cards(handbids):
    hands = list()
    for h in handbids:
        x = [v for v in h.split("") if v != ""]
        cards = x[0]
        bid = x[1]
        hand = Hand(cards, bid)
        hands.append(hand)
    return hands


def test():
    assert Hand.card_value("A") > Hand.card_value("T")
    assert Hand.card_value("K") > Hand.card_value("2")

    h5 = Hand("AAAAA", 1)
    assert h5.rating() == FIVE_OF_A_KIND
    h4 = Hand("22522", 2)
    assert h4.rating() == FOUR_OF_A_KIND
    hfh = Hand("74747", 7)
    assert hfh.rating() == FULL_HOUSE
    h3 = Hand("52322", 6)
    assert h3.rating() == THREE_OF_A_KIND
    h2p = Hand("44233", 11)
    assert h2p.rating() == TWO_PAIR
    hp = Hand("K42K3", 11)
    assert hp.rating() == PAIR
    h0 = Hand("A3579",19)
    assert h0.rating() == HIGHCARD

    assert h5 > h4
    assert h4 > hfh
    assert hfh > h3
    assert h3 > h2p
    assert h2p > hp
    assert hp > h0

    h5b = Hand("99999", 1)
    assert h5b < h5
    h4b = Hand("22322", 2)
    assert h4b < h4
    hfhb = Hand("72727", 7)
    assert hfhb < hfh
    h3b = Hand("92722", 6)
    assert h3 < h3b
    h2pb = Hand("44255", 11)
    assert h2p < h2pb
    hpb = Hand("K42K9", 11)
    assert hp < hpb
    h0b = Hand("A2579",2)
    assert h0b < h0

    assert h0 == h0
    assert h5 == h5
    assert h3b != h3
    assert hp != h4

    print("Test passed")

def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw_lines = f.readlines()
    handbids = [r.strip() for r in raw_lines]
    hands = parse_cards(handbids)
    result = play_cards(hands)
    print(f"cards rank*bid sum is {result}")

if __name__=="__main__":
    main()
