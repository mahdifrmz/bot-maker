import PySimpleGUI as sg

from general import EVENT_HELP_BUTTON, help_button, next_button,back_button,WINDOW_TITLE,EVENT_NEXT_BUTTON,EVENT_BACK_BUTTON
from codegen import BotMakerContext
from help import HELP_PLUGINS, show_help

def runView(context:BotMakerContext) -> bool:
    panel = []

    for i in range(len(context.plugins)):
        panel.append([sg.Checkbox(context.plugins[i].name, context.plugins_selection[i])])
    panel.append([back_button(),next_button()])
    panel.append([help_button()])

    window = sg.Window(WINDOW_TITLE, panel)
    winrsl = True

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_NEXT_BUTTON:
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == sg.WIN_CLOSED:
            exit(0)
        elif event == EVENT_HELP_BUTTON:
            show_help(HELP_PLUGINS)


    for i in range(len(context.plugins)):
        context.plugins_selection[i] = panel[i][0].get()
    
    window.close()
    return winrsl