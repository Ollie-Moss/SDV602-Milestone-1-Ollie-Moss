"""
A comment describing the game module
"""
import PySimpleGUI as sg
import command_parser as cm

# Brief comment about how the following lines work
game_state = 'Forest'
game_places = {'Forest':{'Story':'You are in the forest.\nTo the north is a cave.\nTo the south is a castle',
                        'North':'Cave',
                        'South':'Castle',
                        'Image':'../imgs/forest.png'
                         },
              'Cave':{'Story':'You are at the cave.\nTo the south is forest.',
                        'North':'',
                        'South':'Forest',
                        'Image':'../imgs/forest_circle.png'
                      },
              'Castle':{'Story':'You are at the castle.\nTo the north is forest.',
                        'North':'Forest',
                        'South':'',
                        'Image':'../imgs/frog.png'},
                }

def show_current_place():
    """Gets the story at the game_state place

    Returns:
        string: the story at the current place
    """
    global game_state
    
    return game_places[game_state]['Story']

def game_play(direction):
    """
    Runs the game_play

    Args:
        direction string: _North or South

    Returns:
        string: the story at the current place
    """
    global game_state
    
    if direction.lower() in 'northsouth': # is this a nasty check?
        game_place = game_places[game_state]
        proposed_state = game_place[direction]
        if proposed_state == '' :
            return 'You can not go that way.\n'+game_places[game_state]['Story']
        else :
            game_state = proposed_state
            return game_places[game_state]['Story']
        
    
def make_a_window():
    """
    Creates a game window

    Returns:
        window: the handle to the game window
    """
    
    
    sg.theme('Dark Blue 3')  # please make your windows 
    prompt_input = [
            sg.Text('Enter your command',font='Any 14'), 
            sg.Input(key='-IN-',size=(20,1),font='Any 14')
            ]
    buttons = [
            sg.Button('Enter',  bind_return_key=True), 
            sg.Button('Exit')
            ]
    command_col = sg.Column(
            [prompt_input, buttons], 
            element_justification='r'
            )
    layout = [[sg.Image(r'../imgs/forest.png', subsample=3, size=(600,300),key="-IMG-"), sg.Text(show_current_place(),size=(100,4), font='Any 12', key='-OUTPUT-')],
              [command_col]]

    return  sg.Window('Adventure Game', layout, size=(1366,768))
    

if __name__ == "__main__":
    #testing for now
    # print(show_current_place())
    # current_story = game_play('North')
    # print(show_current_place())
    
    # A persisent window - stays until "Exit" is pressed
    window = make_a_window()

    while True:
        event, values = window.read()
        print(event)
        if event ==  'Enter': 
                cm.parse_command(values['-IN-']);

                if 'North'.lower() in values['-IN-'].lower():
                    current_story = game_play('North')
                    window['-OUTPUT-'].update(current_story)
                elif 'South'.lower() in values['-IN-'].lower():
                    current_story = game_play('South')
                    window['-OUTPUT-'].update(current_story)
                
                window['-IMG-'].update(game_places[game_state]['Image'], subsample=3, size=(600,300))
                pass
        elif event == 'Exit' or event is None or event == sg.WIN_CLOSED:
                break
        else :
                pass
             
    window.close()
    
    
    
    
