from monster_fight import *
from inventory import *
from command_parser import *
import random

# Comes from https://stackoverflow.com/questions/6760685/what-is-the-best-way-of-implementing-singleton-in-python


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


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
    def __init__(self, story, entities=[], items=[], commands={}, neighbours={}, locked=[]):
        self.story = story
        self.items = items
        self.entities = entities
        self.commands = commands
        self.neighbours = neighbours
        self.locked = locked

# ----------- Item Instances -------------


def equipCallback(item, entity):
    if item.equipped:
        item.equipped = False
        stats = useStatIncreaseCallback(
            item, entity, consumed=False, increased=False)
        return f"Unequipped {item.name}!\n" + stats

    if len(list(filter(lambda invItem: invItem.itemType == item.itemType and invItem.equipped, game.player.inventory))) > 0:
        return f"You already have an item of this type equipped!"

    stats = useStatIncreaseCallback(item, entity, consumed=False)
    item.equipped = True
    return f"Equipped {item.name}!\n" + stats


def useStatIncreaseCallback(item, entity, consumed=True, increased=True):
    result = ""
    if consumed:
        result += f"Used {item.name}!\n"
    for stat, value in item.stats.items():
        if increased:
            entity.stats[stat] += item.stats[stat]
            result += f"{stat.title()} increased by {item.stats[stat]}\n"
        else:
            entity.stats[stat] -= item.stats[stat]
            result += f"{stat.title()} decreased by {item.stats[stat]}\n"

    if consumed:
        entity.inventory.remove_item(item.name, 1)

    return result


# ---- Weapons ----

sword = Item("sword", "weapon", {"damage": 3000}, equip=equipCallback)
poison_tipped_sword = Item("poison-tipped-sword",
                           "weapon", {"damage": 100}, equip=equipCallback)

# ---- Armor ----
shield = Item("Shield", "armor", {"defense": 20}, equip=equipCallback)

helmet = Item("helmet", "chest-piece", {"defense": 35}, equip=equipCallback)
chestplate = Item("chestplate", "chest-piece",
                  {"defense": 40}, equip=equipCallback)

# ---- Buff/De-Buffs ----

# Potions
health_potion = Item("health-potion", "potion",
                     {"health": 50}, use=useStatIncreaseCallback)
strength_potion = Item("strength-potion", "potion",
                       {"damage": 25}, use=useStatIncreaseCallback)

# Food
bread_loaf = Item("bread-loaf", "food",
                  {"health": 30}, use=useStatIncreaseCallback)


def keyCallback(item, entity):
    if game.currentLocation == "dungeon":
        return "You have won! The princess is saved!"
# Key


dungeon_key = Item("dungeon-key", "key", {}, use=keyCallback)
# ----------- Monster Instances -----------

goblin = entity(50, None, name="goblin", damage=30)
zombie = entity(75, None, name="zombie", damage=40)
guard = entity(100, None, name="guard", damage=50, defense=30)
vampire = entity(200, None, name="vampire", damage=80,
                 defense=70, drops=[InventoryItem(dungeon_key)])


def handle_move(args):
    if not args:
        return False

    def callback(window):
        window['-RESULT-'].update(f"You moved {args}!")

    if len(game.getCurrentLocation().entities) > 0 and args in game.getCurrentLocation().locked:
        result = "There are still monsters you need to defeat!\n"
        result += ''.join(
            f"{enemy.name.title()}\n" for enemy in game.getCurrentLocation().entities)
        return lambda window: window['-RESULT-'].update(result)
    else:
        if args not in game.getCurrentLocation().neighbours:
            return lambda window: window['-RESULT-'].update(f"You cannot move {args}!")
        game.currentLocation = game.getCurrentLocation().neighbours[args]
        return callback



def handle_equip(args):
    if not args:
        return False

    result = game.player.equipItem(args)

    return lambda window: window['-RESULT-'].update(str(result))


def handle_use(args):
    if not args:
        return False

    result = game.player.useItem(args)

    return lambda window: window['-RESULT-'].update(str(result))
    pass


def handle_inventory(args):
    return lambda window: window['-RESULT-'].update(game.player.inventory.display_items())


def handle_stats(args):
    result = ""
    for stat, value in player.stats.items():
        result += f"{stat}: {value}\n"
    return lambda window: window['-RESULT-'].update(result)


def handle_fight(args):
    if not args:
        return False

    for entity in game.getCurrentLocation().entities:
        if entity.name == args:
            game.fight["enemy"] = entity

            game.getCurrentLocation().commands = {**fight_commands,
                                                  **basic_commands}

            def startFight(window):
                window['-RESULT-'].update(f"Fighting {entity.name}")

            return startFight


def handle_attack(args):
    enemy = game.fight["enemy"]
    if not enemy:
        return lambda window: window['-RESULT-'].update("Not in a fight!")

    playerDamageDealt = game.player.deal_damage(enemy)
    result = f"{game.player.name} hit {enemy.name} for {playerDamageDealt}!\n"
    result += f"{enemy.name} has {enemy.stats['health']} health remaining\n"

    enemyDamageDealt = enemy.deal_damage(game.player)
    result += f"{enemy.name} hit {game.player.name} for {enemyDamageDealt}!\n"
    result += f"{game.player.name} has {game.player.stats['health']} health remaining\n"

    if game.player.stats["health"] <= 0:
        return "RESTART"

    if enemy.stats["health"] <= 0:
        result = f"You have defeated {enemy.name}!\n"
        # Award Drops
        if len(enemy.drops) > 0:
            result += "You have been awarded:"
            for drop in enemy.drops:
                game.player.inventory.add_item(drop)
                result += f"{drop.name} x{drop.quantity}"

        # End Fight
        game.getCurrentLocation().entities.remove(enemy)
        game.fight["enemy"] = None
        game.getCurrentLocation().commands = {**non_fighting_commands,
                                              **basic_commands}

    return lambda window: window['-RESULT-'].update(result)


def handle_run(args):
    enemy = game.fight["enemy"]
    if not enemy:
        return lambda window: window['-RESULT-'].update("Not in a fight!")
    game.fight["enemy"] = None
    game.getCurrentLocation().commands = {**non_fighting_commands,
                                          **basic_commands}
    return lambda window: window['-RESULT-'].update("You have run away!")


def handle_explore(args):
    result = ""
    # Give player random item
    if len(game.getCurrentLocation().items) > 0:
        itemIndex = random.randint(0, len(game.getCurrentLocation().items)-1)
        item = game.getCurrentLocation().items[itemIndex]

        game.player.inventory.add_item(item)
        game.getCurrentLocation().items.remove(item)
        result += f"You have found {item.name}!\n"

    # Show monsters
    if len(game.getCurrentLocation().entities) > 0:
        result += "There are some monsters:"
        result += ''.join(
            f"{enemy.name.title()}\n" for enemy in game.getCurrentLocation().entities)

    # Show moveable directions
    result += "It seems I can move in these directions:\n"
    result += ''.join(f"{direction.title()} leads to {location.title()}\n" if direction not in game.getCurrentLocation(
    ).locked else f"{direction.title()} is being guarded but leads to {location.title()}!\n" for direction, location in game.getCurrentLocation().neighbours.items())

    return lambda window: window['-RESULT-'].update(result)


non_fighting_commands = {
    "move": {
        "callback": handle_move,
        "help": "move [direction]"
    },
    "fight": {
        "callback": handle_fight,
        "help": "fight [monster]"
    },
}

basic_commands = {
    "fight": {
        "callback": handle_fight,
        "help": "fight [monster]"
    },
    "use": {
        "callback": handle_use,
        "help": "fight [monster]"
    },
    "equip": {
        "callback": handle_equip,
        "help": "equip [item]"
    },
    "inventory": {
        "callback": handle_inventory,
        "help": "inventory"
    },
    "stats": {
        "callback": handle_stats,
        "help": "stats or stats [item]"
    },
    "explore": {
        "callback": handle_explore,
        "help": "explore"
    },
}

fight_commands = {
    "attack": {
        "callback": handle_attack,
        "help": "attack"
    },
    "stats": {
        "callback": handle_run,
        "help": "run"
    },
}

game = GameManager(None, None)


def startGame():

    # ---------- Map ---------------

    gameMap = {
        "start": Location(story="Your goal is to save the princess!\nShe is being held in the evil vampire's castle.\nYou must find her, start by exploring you might find something!",
                          commands={**non_fighting_commands, **basic_commands},
                          items=[InventoryItem(sword), InventoryItem(bread_loaf, 2)],
                          locked=["north"],
                          neighbours={"north": "forest"}),
        "forest": Location("This forest seems dense\n It feels like there are eyes everywhere!",
                           commands={**non_fighting_commands,
                                     **basic_commands},
                           locked=["north"],
                           entities=[goblin],
                           neighbours={"north": "castle",
                                       "east": "big tree",
                                       "south": "start"}),
        "big tree": Location(story="This tree is massive, there might be some items around here!",
                             commands={**non_fighting_commands,
                                       **basic_commands},
                             items=[InventoryItem(health_potion, 5), InventoryItem(shield)],
                             locked=["north"],
                             neighbours={"west": "forest"}),
        "castle": Location(story="This castle seems old and dusty, hopefully the princess is near!\n",
                           commands={**non_fighting_commands,
                                     **basic_commands},
                           entities=[guard],
                           items=[InventoryItem(chestplate)],
                           locked=["north"],
                           neighbours={"north": "throne room",
                                       "west": "dungeon",
                                       "south": "forest"}),
        "dungeon": Location(story="The princess must be in here!\nIf only I had the key!",
                            commands={**non_fighting_commands,
                                      **basic_commands},
                            items=[InventoryItem(poison_tipped_sword)],
                            locked=["north"],
                            neighbours={"east": "castle"}),
        "throne room": Location("There's the vampire you must defeat him!",
                                commands={**non_fighting_commands,
                                          **basic_commands},
                                entities=[vampire],
                                locked=["north"],
                                neighbours={"south": "castle"}),
    }

    # ------------ Player Instance ----------

    playerInv = Inventory(
        [])
    player = entity(200, playerInv, name="player")
    game.player = player
    game.map = gameMap
