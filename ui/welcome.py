import PySimpleGUI as sg

from ui.general import WINDOW_TITLE, next_button, EVENT_NEXT_BUTTON

def runView():
    window = sg.Window(WINDOW_TITLE, [[sg.Text('''
    Welcome to Bot Maker!
    This wizard will help you to create a Telegram bot.

    Press next to continue...
                         ''')],[next_button()]]
    )

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_NEXT_BUTTON:
            break
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()