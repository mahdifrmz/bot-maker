import PySimpleGUI as sg

from general import WINDOW_TITLE, next_button, help_button, EVENT_NEXT_BUTTON, EVENT_HELP_BUTTON
from codegen import BotMakerContext
from help import show_help, HELP_WELCOME

def runView(context: BotMakerContext) -> bool:
    window = sg.Window(WINDOW_TITLE, [[sg.Text('''
    Welcome to Bot Maker!
    This wizard will help you to create a Telegram bot.

    Press next to continue...
                         ''')],[next_button()],[help_button()]]
    )

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_NEXT_BUTTON:
            break
        elif event == EVENT_HELP_BUTTON:
            show_help(HELP_WELCOME)
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return True