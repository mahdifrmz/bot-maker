import PySimpleGUI as sg
import os
from pathlib import Path
from codegen import Bot, Generator

WINDOW_TITLE = 'Bot Maker Wizard'
EVENT_NEXT_BUTTON = '_NEXT_'
EVENT_FINISH_BUTTON = '_FINISH_'
STORAGE_PATH = 'storage'

bot = Bot()
bot.storage_root = STORAGE_PATH

def next_button():
    return sg.Button('Next >',key = EVENT_NEXT_BUTTON)

def finish_button():
    return sg.Button('Finish',key = EVENT_FINISH_BUTTON)

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
cancel_message_field = sg.Multiline(size=(45,10))
invalid_message_field = sg.Multiline(size=(45,10))

window = sg.Window(WINDOW_TITLE, [
    [sg.Text('Enter the bot API token you received from the Bot Father:')],
    [token_field],
    [sg.Text('Enter the bot\'s initial "/start" message:')],
    [cancel_message_field],
    [sg.Text('Enter the bot\'s "/help" message:')],
    [invalid_message_field],
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
    elif event == sg.WIN_CLOSED:
        exit(0)

window.close()

# Metadata Form

cancel_message_field = sg.Multiline(size=(45,10))
invalid_message_field = sg.Multiline(size=(45,10))

window = sg.Window(WINDOW_TITLE, [
    [sg.Text('Enter the bot\'s"/cancel" message:')],
    [cancel_message_field],
    [sg.Text('Enter error message for invalid input:')],
    [invalid_message_field],
    [next_button()]
])

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
    elif event == sg.WIN_CLOSED:
        exit(0)

window.close()


# Path Form

bot_path_field = sg.FolderBrowse(key='_PATH_')
bot_name_field = sg.In()

bot_path = ''
bot_name = ''

window = sg.Window(WINDOW_TITLE, [
    [sg.Text('Enter bot name:')],
    [bot_name_field],
    [sg.Text('Enter the path for bot installation:')],
    [bot_path_field],
    [next_button()]
])

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
            bot_name = values[bot_name_field.key]
        if(len(values[bot_path_field.key]) == 0):
            error_empty('path')
            continue
        else:
            bot_path = values[bot_path_field.key]
        break
    elif event == sg.WIN_CLOSED:
        exit(0)

window.close()

# Generate bot

src = Generator().generate(bot)

path = Path.joinpath(Path(bot_path), bot_name)
storage_path = Path.joinpath(path, STORAGE_PATH)
src_path = Path.joinpath(path, 'bot.py')

os.mkdir(path)
os.mkdir(storage_path)
open(src_path,'w').write(src)

# Done

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