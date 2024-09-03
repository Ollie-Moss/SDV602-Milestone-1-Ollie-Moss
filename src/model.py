from monster_fight import *
from inventory import *
from command_parser import *

# ---------------- Model classes ---------


class GameManager:
    def __init__(self, player, map):
        self.player = player
        self.currentLocation = "start"
        self.map = map
        self.fight = {
            "enemy": None
        }

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
    if entity.heldItem == item:
        return f"Item is already equipped!"

    entity.heldItem = item
    return f"Equipped {item.name}"


def useStatIncreaseCallback(item, entity):
    result = ""
    result += f"Used {item.name}!\n"
    for stat, value in item.stats.items():
        entity.stats[stat] += item.stats[stat]
        result += f"{stat.title()} increased by {item.stats[stat]}\n"
    entity.inventory.remove_item(item.name, 1)

    return result


# ---- Weapons ----

sword = Item("sword", "weapon", {"damage": 30}, equip=equipCallback)
bow = Item("bow", "weapon", {"damage": 15}, equip=equipCallback)

# ---- Armor ----
shield = Item("Shield", "armor", {"defense": 20})

helmet = Item("helmet", "armor", {"defense": 30})

# ---- Buff/De-Buffs ----

# Potions
health_potion = Item("health-potion", "potion",
                     {"health": 50}, use=useStatIncreaseCallback)

# Food
grapes = Item("grapes", "food", {"health": 25}, use=useStatIncreaseCallback)
bread_loaf = Item("bread-loaf", "food",
                  {"health": 30}, use=useStatIncreaseCallback)

# ----------- Monster Instances -----------

goblin = entity(50, None, name="goblin")
zombie = entity(75, None, name="zombie")
guard = entity(100, None, name="guard")
vampire = entity(200, None, name="vampire")


def handle_move(args):
    def callback(window):
        window['-STORY-'].update(game.getCurrentLocation().story)
    args = args[0]

    if len(game.getCurrentLocation().entities) > 0:
        return lambda window: window['-RESULT-'].update("There are still monsters you need to defeat!")
    else:
        game.currentLocation = game.getCurrentLocation().neighbours[args]
        return callback

    print("Usage: move [direction]")


def handle_equip(args):
    result = game.player.equipItem(args[0])

    return lambda window: window['-RESULT-'].update(str(result))


def handle_use(args):
    result = game.player.useItem(args[0])

    return lambda window: window['-RESULT-'].update(str(result))
    pass


def handle_inventory(args):
    return lambda window: window['-RESULT-'].update(player.inventory.display_items())


def handle_stats(args):
    result = ""
    for stat, value in player.stats.items():
        result += f"{stat}: {value}\n"
    return lambda window: window['-RESULT-'].update(result)


def handle_fight(args):
    for entity in game.getCurrentLocation().entities:
        if entity.name == args[0]:
            game.fight["enemy"] = entity

        game.getCurrentLocation().commands = fightCommands
        def startFight(window):
            commands = [list(map(lambda command: sg.Text(f"{command}", font="Any 12", background_color="#FFFFFF", text_color="#000000"),
                   game.getCurrentLocation().commands.keys()))]
            window['-COMMANDS-'].update(commands)
            window['-RESULT-'].update(f"Fighting {entity.name}")

        return startFight


def handle_attack(args):
    enemy = game.fight["enemy"]
    if not enemy:
        return lambda window: window['-RESULT-'].update("Not in a fight!")

    game.player.deal_damage(enemy)
    return lambda window: window['-RESULT-'].update(f"Hit {enemy.name}")


def handle_heal(args):
    pass


def handle_run(args):

    pass


basicCommands = {
    "move": handle_move,
    "equip": handle_equip,
    "use": handle_use,
    "inventory": handle_inventory,
    "stats": handle_stats,
    "fight": handle_fight
}

fightCommands = {
    "attack": handle_attack,
    "heal": handle_heal,
    "run": handle_run
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
