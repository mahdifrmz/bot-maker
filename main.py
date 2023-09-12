import PySimpleGUI as sg
from codegen import Bot

WINDOW_TITLE = 'Bot Maker Wizard'

EVENT_NEXT_BUTTON = '_NEXT_'

bot = Bot()

def next_button():
    return sg.Button('Next >',key = EVENT_NEXT_BUTTON)

def error_empty(field:str):
    sg.popup_ok(field + ' field must be filled',title='Error')

# Welcome Form

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

# Credentials Form

token_field = sg.In()
start_message_field = sg.Multiline(size=(45,10))
help_message_field = sg.Multiline(size=(45,10))

window = sg.Window(WINDOW_TITLE, [
    [sg.Text('Enter the bot API token you received from the Bot Father:')],
    [token_field],
    [sg.Text('Enter the bot\'s initial "/start" message:')],
    [start_message_field],
    [sg.Text('Enter the bot\'s initial "/help" message:')],
    [help_message_field],
    [next_button()]
])

while True:
    ev = window.read()
    if ev == None:
        continue
    event, values = ev
    if event == EVENT_NEXT_BUTTON:
        if(len(token_field.get()) == 0):
            error_empty('token')
            continue
        else:
            bot.token = token_field.get()
        if(len(start_message_field.get()) == 0):
            error_empty('start message')
            continue
        else:
            bot.resp_start = start_message_field.get()
        if(len(help_message_field.get()) == 0):
            error_empty('help')
            continue
        else:
            bot.resp_help = help_message_field.get()
        break
    elif event == sg.WIN_CLOSED:
        exit(0)

window.close()