import PySimpleGUI as sg
from model import *

def parse_command(command):
    command = command.lower().split(' ')
    action = command[0]
    if action not in game.getCurrentLocation().commands:
        return
    args = command[1:]
    if len(args) > 0:
        args = args[0]
    else:
        args = None
    return game.getCurrentLocation().commands[action](args)


