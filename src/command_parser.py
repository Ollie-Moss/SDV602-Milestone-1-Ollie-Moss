import PySimpleGUI as sg
from status import *


def parse_command(command):
    command = command.lower().split(' ')
    action = command[0]
    if action not in game.getCurrentLocation().commands:
        return
    args = command[1:]
    return game.getCurrentLocation().commands[action](args)


