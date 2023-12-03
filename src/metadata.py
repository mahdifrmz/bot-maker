import PySimpleGUI as sg

from codegen import Bot, BotMakerContext
from general import EVENT_HELP_BUTTON, WINDOW_TITLE, help_button, next_button, back_button, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON, error_empty
from help import HELP_METADATA, show_help

def runView(context:BotMakerContext) -> bool:
    
    cancel_message_field = sg.Multiline(size=(45,10), default_text=context.bot.resp_cancel)
    invalid_message_field = sg.Multiline(size=(45,10), default_text=context.bot.resp_invalid)

    window = sg.Window(WINDOW_TITLE, [
        [sg.Text('Enter the bot\'s"/cancel" message:')],
        [cancel_message_field],
        [sg.Text('Enter error message for invalid input:')],
        [invalid_message_field],
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
            if(len(cancel_message_field.get()) == 0):
                error_empty('cancel message')
                continue
            else:
                context.bot.resp_cancel = cancel_message_field.get()
            if(len(invalid_message_field.get()) == 0):
                error_empty('error')
                continue
            else:
                context.bot.resp_invalid = invalid_message_field.get()
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == sg.WIN_CLOSED:
            exit(0)
        elif event == EVENT_HELP_BUTTON:
            show_help(HELP_METADATA)

    window.close()
    return winrsl