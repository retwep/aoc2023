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
        self.natural = cards
        self.pretend = self.apply_jokers(cards)
        self.bid = bid
        self.rank = 0  # filled in later

    @staticmethod
    def card_value(c) -> int:
        values = "J23456789TQKA"
        assert c in values
        return values.find(c)

    def apply_jokers(self, cards) -> str:
        self.category = Hand.rating(cards)
        if "J" not in cards:
            self.pretend = cards
            return cards

        # create a bunch of options and pick the best
        best_cards = cards
        best_rating = self.category

        def keep_best(nc):
            nonlocal best_cards, best_rating
            nr = Hand.rating(nc)
            if nr > best_rating:  # new card rating wins
                best_cards = nc
                best_rating = nr
            elif nr == best_rating:  # pick the best cards at this same rating
                if Hand.card_compare_lt(best_cards, nc): # best is less than new cards
                    best_cards = nc
                    best_rating = nr


        # for every card that is a joker, try replacing it with an A
        keep_best(cards.replace("J", "A"))

        # for every card that is a joker, try replacing it with one of the other cards in the hand
        mix = set(list(cards))
        for i, c in enumerate(mix):
            if c == "J":
                continue
            keep_best(cards.replace("J", c))
        self.category = best_rating
        self.pretend = best_cards
        return best_cards

    @staticmethod
    def rating_dict(cards: str):
        d = dict()
        for card in cards:
            if d.get(card) is None:
                d[card] = 1
            else:
                d[card] += 1
        return d

    @staticmethod
    def rating(cards):
        d = Hand.rating_dict(cards)
        if len(d) == 1:
            # 5 of a kind
            return FIVE_OF_A_KIND
        if len(d) == 2:
            # four or fullhouse
            if d[cards[0]] in [3,2]:
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

    @staticmethod
    def card_compare_lt(c1, c2):
        # caller must make sure they have the same rating category!
        for a,b in zip(list(c1), list(c2)):
            if Hand.card_value(a) < Hand.card_value(b):
                return True
            elif Hand.card_value(a) > Hand.card_value(b):
                return False
        return False # equal, not less than.

    def __lt__(self, x:"Hand"):
        if self.category < x.category:
            return True
        if self.category > x.category:
            return False
        for a,b in zip(list(self.natural), list(x.natural)):
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
    def __eq__(self, x:"Hand"):
        if self.category != x.category:
            return False
        for a,b in zip(list(self.natural), list(x.natural)):
            if self.card_value(a) != self.card_value(b):
                return False
        return True # equal
    
    def stronger_hand(self, b):
        if self < b:
            return -1
        if b < self:
            return 1
        return 0

def play_cards(hands) -> int:
    def print_hands(title:str, hands:Hand):
        print(title)
        for h in hands:
            print(f"{h.natural}, {h.pretend}, {h.bid=}, {h.rank=} ")

    print_hands("unranked", hands)
    sorted_hands = sorted(hands)
    for i,v in enumerate(sorted_hands):
        v.rank = i+1
    print_hands("ranked", sorted_hands)
    winnings = 0
    for h in hands:
        winnings += h.rank * h.bid
    return winnings

def parse_cards(handbids):
    hands = list()
    for h in handbids:
        x = [v for v in h.split(" ") if v != ""]
        cards = x[0]
        bid = int(x[1])
        hand = Hand(cards, bid)
        hands.append(hand)
    return hands


def test():
    assert Hand.card_value("A") > Hand.card_value("T")
    assert Hand.card_value("K") > Hand.card_value("2")

    h5 = Hand("AAAAA", 1)
    assert h5.category == FIVE_OF_A_KIND
    h4 = Hand("22522", 2)
    assert h4.category == FOUR_OF_A_KIND
    hfh = Hand("74747", 7)
    assert hfh.category == FULL_HOUSE
    h3 = Hand("52322", 6)
    assert h3.category == THREE_OF_A_KIND
    h2p = Hand("44233", 11)
    assert h2p.category == TWO_PAIR
    hp = Hand("K42K3", 11)
    assert hp.category == PAIR
    h0 = Hand("A3579",19)
    assert h0.category == HIGHCARD

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

    hands = parse_cards([" AAAAA   17  "])
    assert len(hands) == 1
    assert hands[0].category == FIVE_OF_A_KIND
    assert hands[0].bid == 17
    hands = parse_cards(["AKQJT 3", " 99977 9  ", "JJJJJ 5", "JJJJA 7", "AAKKJ 6"])
    assert len(hands) == 5
    assert hands[0].category == PAIR
    assert hands[0].bid == 3
    assert hands[1].category == FULL_HOUSE
    assert hands[1].bid == 9
    assert hands[2].category == FIVE_OF_A_KIND
    assert hands[3].category == FIVE_OF_A_KIND
    assert hands[4].category == FULL_HOUSE
    assert hands[4].pretend == "AAKKA"

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
