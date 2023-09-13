import PySimpleGUI as sg
import os
from pathlib import Path
from codegen import Bot, Generator, Command, Step

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

# Commands Form

commands_list = []

commands_listbox = sg.Listbox(commands_list, size=(45,10))
command_name = sg.In()
command_success_message = sg.Multiline(size=(45,10))
add_command_button = sg.Button('Add', key='_ADD_COMMAND_')
delete_command_button = sg.Button('Delete', key='_DEL_COMMAND_')

command_panel = [
    [sg.Text('Commands:')],
    [commands_listbox],
    [sg.Text('\nCreate new command:\n')],
    [sg.Text('Name:')],
    [command_name],
    [sg.Text('Success Message:')],
    [command_success_message],
    [add_command_button,delete_command_button,next_button()]
]

steps_list = []

steps_list = sg.Listbox(steps_list, size=(45,10))
step_question = sg.In()
step_media = sg.Combo(['Text','Image','Video','Audio','Document'])
add_step_button = sg.Button('Add', key='_ADD_STEP_')
delete_step_button = sg.Button('Delete', key='_DEL_STEP_')

step_panel = [
    [sg.Text('Steps:')],
    [steps_list],
    [sg.Text('\nCreate new step:\n')],
    [sg.Text('Success Message:')],
    [step_question],
    [sg.Text('Media type:')],
    [step_media],
    [add_step_button,delete_step_button]
]

window = sg.Window(WINDOW_TITLE, [[
    sg.Column(command_panel),
    sg.VerticalSeparator(),
    sg.Column(step_panel),
]])


def hasCommand(bot:Bot, command_name:str) -> bool:
    for cmd in bot.commands:
        if cmd.name == command_name:
            return True
    return False

while True:
    ev = window.read()
    if ev == None:
        continue
    event, values = ev
    if event == EVENT_NEXT_BUTTON:
        break
    elif event == add_command_button.key:
        fieldName = command_name.get()
        fieldSucMes = command_success_message.get()
        if(len(fieldName) == 0):
            error_empty('command name')
        elif(len(fieldSucMes) == 0):
            error_empty('command success message')
        elif(hasCommand(bot,fieldName)):
            sg.popup_ok('Command names must be unique',title='Error')
        else:
            bot.commands.append(Command(fieldName,fieldSucMes))
            commands_list.append(fieldName)
            commands_listbox.update(commands_list)
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