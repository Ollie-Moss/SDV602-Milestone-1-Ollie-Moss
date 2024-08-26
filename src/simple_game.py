"""
A comment describing the game module
"""
import PySimpleGUI as sg
from command_parser import *


def make_a_window():
    """
    Creates a game window

    Returns:
        window: the handle to the game window
    """

    sg.theme('Dark Blue 3')  # please make your windows
    prompt_input = [
        sg.Text('Enter your command', font='Any 14'),
        sg.Input(key='-IN-', size=(20, 1), font='Any 14')
    ]
    buttons = [
        sg.Button('Enter',  bind_return_key=True),
        sg.Button('Exit')
    ]
    command_col = sg.Column(
        [prompt_input, buttons],
        element_justification='r'
    )
    layout = [
        [sg.Text(f"{game.getCurrentLocation().story}", size=(
            100, 10), font='Any 12', key='-STORY-')],
        [sg.Text("", size=(100, 4), font="Any 12", key='-INV-')],
        [sg.Text(f"", size=(100, 4), font="Any 12", key='-PLAYERSTATS-')],
        [command_col]]

    return sg.Window('Adventure Game', layout, size=(1366, 768))


if __name__ == "__main__":
    # testing for now
    # print(show_current_place())
    # current_story = game_play('North')
    # print(show_current_place())

    # A persisent window - stays until "Exit" is pressed
    window = make_a_window()
    while True:
        event, values = window.read()
        print(event)
        if event == 'Enter':
            result = parse_command(values['-IN-'])
            if (callable(result)):
                result(window)

            pass
        elif event == 'Exit' or event is None or event == sg.WIN_CLOSED:
            break
        else:
            pass

    window.close()
