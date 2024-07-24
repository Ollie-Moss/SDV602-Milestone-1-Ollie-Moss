import monster_fight as mf
import inventory as inv
import status as st

def parse_command(command):
    match command.lower():
        case "north":
            print("North");
            return;
        case "south":
            print("South");
            return;
        case "east":
            print("East");
            return;
        case "west":
            print("West");
            return;
        case _:
            return;
