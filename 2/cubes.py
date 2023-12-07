#!/usr/bin/env python
import sys
from box import Box

target = Box({"red": 12, "green": 13, "blue": 14})
class CubeGame(Box):
    @staticmethod
    def parse_game(value: str):
        id,draws = value.split(":")
        game = CubeGame()
        game.id = int(id.split(" ")[1])
        raw_draws = draws.split(";")
        game.draws = list()
        for raw_draw in raw_draws:
            colors = raw_draw.split(",")
            draw = Box()
            draw.red = 0
            draw.green = 0
            draw.blue = 0
            for raw_color in colors:
                count, color = raw_color.strip().split(" ")
                draw[color] = int(count)
            game.draws.append(draw)
        return game
        
    def validate(self, target):
        for draw in self.draws:
            if draw.red > target.red or draw.green > target.green or draw.blue > target.blue:
                return False
        return True
    
    def power(self):
        red = max(draw.red for draw in self.draws)
        green = max(draw.green for draw in self.draws)
        blue = max(draw.blue for draw in self.draws)
        power = red * green * blue
        print(f"{self.id=} power({red}, {green}, {blue})={power}")
        return power


def test():
    global target

    print(f'{CubeGame.parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")}')
    print("****")

    games = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]

    for gs in games:
        game = CubeGame.parse_game(gs)
        print(f"{game.id=}, {game.draws[0].red=}, {game.draws[0].green=} {game.draws[0].blue=} result: {game.validate(target)}, power: {game.power()}")

    
def main():
    global target
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw = f.readlines()
    games = list()
    sum = 0
    power = 0
    for line in raw:
        game = CubeGame.parse_game(line)
        if game.validate(target):
            sum += game.id
        power += game.power()

    print(f"{sum=}, {power=}")

if __name__=="__main__":
    main()
