import PySimpleGUI as sg

from ui.general import WINDOW_TITLE, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON, error_empty, next_button, back_button
from codegen import Bot

def runView(bot:Bot) -> bool:
    
    token_field = sg.In(default_text=bot.token)
    cancel_message_field = sg.Multiline(default_text=bot.resp_cancel, size=(45,10))
    invalid_message_field = sg.Multiline(default_text=bot.resp_invalid, size=(45,10))

    window = sg.Window(WINDOW_TITLE, [
        [sg.Text('Enter the bot API token you received from the Bot Father:')],
        [token_field],
        [sg.Text('Enter the bot\'s initial "/start" message:')],
        [cancel_message_field],
        [sg.Text('Enter the bot\'s "/help" message:')],
        [invalid_message_field],
        [back_button(), next_button()]
    ])

    winrsl = True

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, value = ev
        if event == EVENT_NEXT_BUTTON:
            if(len(token_field.get()) == 0):
                error_empty('token')
                continue
            else:
                bot.token = token_field.get()
            if(len(cancel_message_field.get()) == 0):
                error_empty('start message')
                continue
            else:
                bot.resp_start = cancel_message_field.get()
            if(len(invalid_message_field.get()) == 0):
                error_empty('help')
                continue
            else:
                bot.resp_help = invalid_message_field.get()
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return winrsl