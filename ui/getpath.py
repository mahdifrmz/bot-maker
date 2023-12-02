import PySimpleGUI as sg

from ui.general import WINDOW_TITLE, next_button, back_button, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON, error_empty

def runView(botOutput: list[str]) -> bool:
    bot_path_field = sg.FolderBrowse(key='_PATH_')
    bot_name_field = sg.In(key='__BNAME__', default_text=botOutput[1])

    window = sg.Window(WINDOW_TITLE, [
        [sg.Text('Enter bot name:')],
        [bot_name_field],
        [sg.Text('Enter the path for bot installation:')],
        [bot_path_field],
        [back_button(), next_button()]
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
                botOutput[1] = values[bot_name_field.key]
            if(len(values[bot_path_field.key]) == 0):
                error_empty('path')
                continue
            else:
                botOutput[0] = values[bot_path_field.key]
            break
        elif event == EVENT_NEXT_BUTTON:
            winrsl = False
            break
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return winrsl