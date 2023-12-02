import PySimpleGUI as sg

from codegen import Bot
from ui.general import WINDOW_TITLE, next_button, back_button, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON, error_empty

def runView(bot: Bot) -> bool:
    
    cancel_message_field = sg.Multiline(size=(45,10), default_text=bot.resp_cancel)
    invalid_message_field = sg.Multiline(size=(45,10), default_text=bot.resp_invalid)

    window = sg.Window(WINDOW_TITLE, [
        [sg.Text('Enter the bot\'s"/cancel" message:')],
        [cancel_message_field],
        [sg.Text('Enter error message for invalid input:')],
        [invalid_message_field],
        [back_button(), next_button()]
    ])

    winrsl = True
    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_NEXT_BUTTON:
            if(len(cancel_message_field.get()) == 0):
                error_empty('cancel message')
                continue
            else:
                bot.resp_cancel = cancel_message_field.get()
            if(len(invalid_message_field.get()) == 0):
                error_empty('error')
                continue
            else:
                bot.resp_invalid = invalid_message_field.get()
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return winrsl