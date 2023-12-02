import PySimpleGUI as sg
from general import WINDOW_TITLE, finish_button, EVENT_FINISH_BUTTON
from codegen import BotMakerContext
def runView(context: BotMakerContext) -> bool:
    window = sg.Window(WINDOW_TITLE, [[sg.Text('''
    Bot generated successfully!
                         ''')],[finish_button()]]
    )

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_FINISH_BUTTON:
            break
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return True