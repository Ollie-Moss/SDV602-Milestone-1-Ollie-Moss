import PySimpleGUI as sg
import monster_fight as mf
from inventory import *
import status as st


def parse_command(command):
    command = command.lower().split(' ')
    action = command[0]
    args = command[1:]
    return commandCallBacks[action](args)


def handle_move(args):
    def callback(window):
        window['-STORY-'].update(game.getCurrentLocation().story)
        window['-PLAYERSTATS-'].update(f"x: {game.player.x} y: {game.player.y}")
    args = args[0]
    if args in directionCallBacks:
        directionCallBacks[args](player)
        return callback
    else:
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


directionCallBacks = {
    "north": lambda player: player.move([0, -1]) if game.player.y > 0 else print(""),
    "east": lambda player: player.move([1, 0])if game.player.y < len(game.map.matrix[0]) else print(""),
    "south": lambda player: player.move([0, 1])if game.player.y < len(game.map.matrix) else print(""),
    "west": lambda player: player.move([-1, 0])if game.player.x > 0 else print("")
}

commandCallBacks = {
    "move": handle_move,
    "equip": handle_equip,
    "use": handle_use,
    "inventory": handle_inventory,
    "attack": handle_attack
}


def swordCallback(item, player):
    player.heldItem = item
sword = Item("sword", "weapon", {"damage": 100}, equip=swordCallback)


helmet = Item("helmet", "armor", {"defense": 30})

grapes = Item("grape", "food", {"health": 25})

bread_loaf = Item("bread loaf", "food", {"health": 100})

playerInv = Inventory(
    [InventoryItem(sword, 1), InventoryItem(helmet, 1), InventoryItem(grapes, 12), InventoryItem(bread_loaf, 3)])
player = mf.entity(100, playerInv)
game = st.GameManager(player)
