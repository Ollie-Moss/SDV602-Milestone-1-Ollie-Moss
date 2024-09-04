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
        sg.Text('Enter your command', font='Any 12'),
        sg.Input(key='-IN-', size=(20, 1), font='Any 12')
    ]
    buttons = [
        sg.Button('Enter',  bind_return_key=True),
        sg.Button('Exit')
    ]
    command_col = sg.Column(
        [prompt_input, buttons],
        element_justification='r'
    )

    commands = ''.join(
        f"{command} " for command in game.getCurrentLocation().commands.keys())

    layout = [
        [sg.Text("Story:", font="Any 12")],
        [sg.Text(f"{game.getCurrentLocation().story}",
                 size=(100, 5), font='Any 12', key='-STORY-')],
        [sg.Text("Output:", font="Any 12")],
        [sg.Text("",
                 size=(100, 7), background_color="#FFFFFF", text_color="#000000", font="Any 12", key='-RESULT-')],
        [sg.Text("", size=(100, 4), font="Any 12", key='-PLAYERSTATS-')],
        [sg.Text("Available Commands:", font="Any 12"), sg.Text("Type help after any command to see how to use it!")],
        [sg.Text(commands, font="Any 12", background_color="#FFFFFF",
                 text_color="#000000", key="-COMMANDS-")],
        [command_col]]

    return sg.Window('Adventure Game', layout, size=(700, 600))


def resetWindow(window):
    pass


if __name__ == "__main__":
    # testing for now
    # print(show_current_place())
    # current_story = game_play('North')
    # print(show_current_place())

    # A persisent window - stays until "Exit" is pressed
    startGame()
    window = make_a_window()
    while True:
        event, values = window.read()
        print(event)
        if event == 'Enter':
            result = parse_command(values['-IN-'])
            if (callable(result)):
                result(window)

            window['-STORY-'].update(game.getCurrentLocation().story)
            commands = ''.join(
                f"{command} " for command in game.getCurrentLocation().commands.keys())
            window['-COMMANDS-'].update(commands)

            if result == "RESTART":
                game = startGame()
                resetWindow(window)


            pass
        elif event == 'Exit' or event is None or event == sg.WIN_CLOSED:
            break
        else:
            pass

    window.close()
