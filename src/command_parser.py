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
    if args == "help":
        return lambda window: window['-RESULT-'].update(f"Usage: {game.getCurrentLocation().commands[action]['help']}")

    result = game.getCurrentLocation().commands[action]["callback"](args)
    if not result:
        return lambda window: window['-RESULT-'].update(f"Usage: {game.getCurrentLocation().commands[action]['help']}")
    return result
