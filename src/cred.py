import PySimpleGUI as sg

from general import EVENT_HELP_BUTTON, WINDOW_TITLE, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON, error_empty, help_button, next_button, back_button
from codegen import BotMakerContext
from help import show_help, HELP_CREDENTIALS

def runView(context: BotMakerContext) -> bool:
    
    token_field = sg.In(default_text=context.bot.token)
    cancel_message_field = sg.Multiline(default_text=context.bot.resp_start, size=(45,10))
    invalid_message_field = sg.Multiline(default_text=context.bot.resp_help, size=(45,10))

    window = sg.Window(WINDOW_TITLE, [
        [sg.Text('Enter the bot API token you received from the Bot Father:')],
        [token_field],
        [sg.Text('Enter the bot\'s initial "/start" message:')],
        [cancel_message_field],
        [sg.Text('Enter the bot\'s "/help" message:')],
        [invalid_message_field],
        [back_button(), next_button()],
        [help_button()]
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
                context.bot.token = token_field.get()
            if(len(cancel_message_field.get()) == 0):
                error_empty('start message')
                continue
            else:
                context.bot.resp_start = cancel_message_field.get()
            if(len(invalid_message_field.get()) == 0):
                error_empty('help')
                continue
            else:
                context.bot.resp_help = invalid_message_field.get()
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == EVENT_HELP_BUTTON:
            show_help(HELP_CREDENTIALS)
        elif event == sg.WIN_CLOSED:
            exit(0)

    window.close()
    return winrsl