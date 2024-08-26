from monster_fight import *
from inventory import *

# ---------------- Status classes ---------


class GameManager:
    def __init__(self, player, map):
        self.player = player
        self.isFighting = False
        self.currentLocation = "start"
        self.map = map

    def getCurrentLocation(self):
        return self.map[self.currentLocation]


class Location:
    def __init__(self, story, entities, commands, neighbours):
        self.story = story
        self.entities = entities
        self.commands = commands
        self.neighbours = neighbours

# ----------- Item Instances -------------


def equipCallback(item, entity):
    entity.heldItem = item

# ---- Weapons ----


sword = Item("sword", "weapon", {"damage": 30}, equip=equipCallback)
bow = Item("bow", "weapon", {"damage": 15}, equip=equipCallback)

# ---- Armor ----
shield = Item("Shield", "armor", {"defense": 20})

helmet = Item("helmet", "armor", {"defense": 30})

# ---- Buff/De-Buffs ----

# Potions
health_potion = Item("health potion", "potion", {"health": 50})

# Food
grapes = Item("grapes", "food", {"health": 25})
bread_loaf = Item("bread loaf", "food", {"health": 30})

# ----------- Monster Instances -----------

goblin = entity(50, None)
zombie = entity(75, None)
guard = entity(100, None)
vampire = entity(200, None)


def handle_move(args):
    def callback(window):
        window['-STORY-'].update(game.getCurrentLocation().story)
    args = args[0]

    game.currentLocation = game.getCurrentLocation().neighbours[args]
    return callback

    print("Usage: move [direction]")


def handle_equip(args):
    player.equipItem(args[0])


def handle_use(args):
    pass


def handle_inventory(args):
    global game
    return lambda window: window['-INV-'].update(player.inventory.display_items())


def handle_attack(args):
    pass


basicCommands = {
    "move": handle_move,
    "equip": handle_equip,
    "use": handle_use,
    "inventory": handle_inventory,
}

# ---------- Map ---------------

gameMap = {
    "start": Location("Your goal is to save the princess!\nShe is being held in the evil vampire's castle.\nYou must find her, start by moving north!",
                      [],
                      basicCommands,
                      {"north": "forest"}),
    "forest": Location("This forest seems dense, it feels like there are eyes everywhere!\n",
                       [goblin],
                       basicCommands,
                       {"north": "castle",
                        "south": "start"}),
    "castle": Location("This castle seems old and dusty, hopefully the princess is near!\n",
                       [guard],
                       basicCommands,
                       {"north": "throne room",
                        "south": "forest"}),
    "throne room": Location("Ahhhh a vampire he scary!",
                        [vampire],
                        basicCommands,
                        {"north": "end",
                         "south": "castle"}),
    "end": Location("You Win!", [], {}, {})
}

# ------------ Player Instance ----------

playerInv = Inventory(
    [InventoryItem(sword), InventoryItem(helmet), InventoryItem(grapes, 12), InventoryItem(bread_loaf, 3)])
player = entity(100, playerInv)
game = GameManager(player, gameMap)
