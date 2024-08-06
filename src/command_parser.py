import monster_fight as mf
import inventory as inv
import status as st


def parse_command(command):
    command = command.lower().split(' ')
    action = command[0]
    args = command[1:]
    match action:
        case "move":
            return handle_move(args)
        case "equip":
            return handle_equip(args)
        case "use":
            return handle_use(args)
        case "inventory":
            return handle_inventory()
        case "attack":
            return handle_attack()


def handle_move(args):
    if args is list:
        args = args[0]
    match args:
        case "north":
            print("North")
            return
        case "south":
            print("South")
            return
        case "east":
            print("East")
            return
        case "west":
            print("West")
            return
        case _:
            print("Command Not Found!")
            return


def handle_equip():
    pass


def handle_use():
    pass


def handle_inventory():
    global game
    return game.player.inventory.display_items()


def handle_attack():
    pass


sword = inv.Item("sword", "weapon", {"damage": 100})
helmet = inv.Item("helmet", "armor", {"defense": 30})
grapes = inv.Item("grape", "food", {"health": 25})
bread_loaf = inv.Item("bread loaf", "food", {"health": 100})

playerInv = inv.Inventory(
    [[sword, 1], [helmet, 1], [grapes, 12], [bread_loaf, 3]])
player = mf.entity(100, playerInv)
game = st.GameManager(player)

print(game.getCurrentLocation().story)
game.map.printMap()
