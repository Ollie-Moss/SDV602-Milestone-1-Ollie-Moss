class GameManager:
    def __init__(self, player):
        self.running = False
        self.map = Map()
        self.player = player
        self.state = State()

    def getCurrentLocation(self):
        return self.map.matrix[(self.player.y)][int(self.player.x)]


class Map:
    def __init__(self):
        self.matrix = [[Location("top left"), Location("top right")],
                       [Location("bottom left"), Location("bottom right")]]

    def printMap(self):
        result = ""
        tile_size = 1
        for row in self.matrix:
            for location in row:
                if len(location.story) > tile_size:
                    tile_size = len(location.story)

        for x in range(0, len(self.matrix[0])):
            result += "+" + "-"*(tile_size+2)
            print("+" + "-"*(tile_size+2), end="")
        result += "+\n"
        print("+")
        for row in self.matrix:
            for location in row:
                result += f'| {location.story:{tile_size}} '
                print(f'| {location.story:{tile_size}} ', end="")
            result += "|\n"
            print("|")
            for x in range(0, len(self.matrix[0])):
                result += "+" + "-"*(tile_size+2)
                print("+" + "-"*(tile_size+2), end="")
            result += "+\n"
            print("+")
        print(result)
        return result


class Location:
    def __init__(self, story="There is no story", image="", entities=[], commands=()):
        self.story = story
        self.image = image
        self.entities = entities
        self.commands = commands


class State:
    def __init__(self):
        self.fighting = False
        self.x = 0
        self.y = 0
