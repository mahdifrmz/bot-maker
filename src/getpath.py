import PySimpleGUI as sg

from general import EVENT_HELP_BUTTON, WINDOW_TITLE, help_button, next_button, back_button, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON, error_empty
from codegen import BotMakerContext
from help import HELP_GETPATH, show_help

def runView(context: BotMakerContext) -> bool:
    bot_path_field = sg.FolderBrowse(key='_PATH_')
    bot_name_field = sg.In(key='__BNAME__', default_text=context.botOutput[1])

    window = sg.Window(WINDOW_TITLE, [
        [sg.Text('Enter bot name:')],
        [bot_name_field],
        [sg.Text('Enter the path for bot installation:')],
        [bot_path_field],
        [back_button(), next_button()],
        [help_button()]
    ])

    winrsl = True

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_NEXT_BUTTON:
            if(len(bot_name_field.get()) == 0):
                error_empty('name')
                continue
            else:
                context.botOutput[1] = values[bot_name_field.key]
            if(len(values[bot_path_field.key]) == 0):
                error_empty('path')
                continue
            else:
                context.botOutput[0] = values[bot_path_field.key]
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == EVENT_HELP_BUTTON:
            show_help(HELP_GETPATH)
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return winrsl