import monster_fight as mf
import inventory as inv
import status as st

def parse_command(command):
    command = command.lower().split(' ')
    action = command[0]
    args = command[1:]
    match action:
        case "move":
            handle_move(args)
            return
        case "equip":
            handle_equip()
            return
        case "use":
            handle_use()
            return
        case "inventory":
            handle_inventory()
            return
        case "attack":
            handle_attack()
            return

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

def handle_use():
    pass

def handle_use():
    pass

def handle_use():
    pass

def handle_use():
    pass

