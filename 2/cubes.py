import sys
from box import Box


class CubeGame(Box):
    @staticmethod
    def parse_game(value: str):
        id,draws = value.split(":")
        game = CubeGame()
        game.id = id.split(" ")[1]
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
                draw[color] = count
            game.draws.append(draw)
        
    def validate(self):
        pass

def test():
    target = Box({"red": 12, "green": 13, "blue": 14})

    print(f'{CubeGame.parse_game("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")}')
    games = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]

    for gs in games:
        game = CubeGame.parse_game(gs)
        print(f"{game.Game=}, {game.red=}, {game.green=} {game.blue=}{game.validate()}")


def main():
    if len(sys.argv) < 2:
        test()
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        raw = f.readlines()
    games = list()
    sum = 0
    for line in raw:
        game = CubeGame.parse_game(line)
        if game.validate():
            sum += game.id
    print(f"{sum=}")

if __name__=="__main__":
    main()
