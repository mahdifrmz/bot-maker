import PySimpleGUI as sg
import os
from pathlib import Path
from codegen import Bot, Generator, Command, Step

WINDOW_TITLE = 'Bot Maker Wizard'
EVENT_NEXT_BUTTON = '_NEXT_'
EVENT_FINISH_BUTTON = '_FINISH_'
STORAGE_PATH = 'storage'
MEDIA_TYPES = ['Text','Image','Audio','Video','Document']

bot = Bot()
bot.storage_root = STORAGE_PATH

def next_button():
    return sg.Button('Next >',key = EVENT_NEXT_BUTTON)

def finish_button():
    return sg.Button('Finish',key = EVENT_FINISH_BUTTON)

def valid_media_type(name:str) -> int:
    i = 0
    for mt in MEDIA_TYPES:
        i += 1
        if mt == name:
            return i
    return -1


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

commands_listbox = sg.Listbox(commands_list, enable_events=True, key='_LIST_COMMAND_', size=(45,10))
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

steps_listbox = sg.Listbox(steps_list, enable_events=True, key='_LIST_STEP_', size=(45,10))
step_question = sg.Multiline(size=(45,10))
step_media = sg.Combo(MEDIA_TYPES)
add_step_button = sg.Button('Add', key='_ADD_STEP_')
delete_step_button = sg.Button('Delete', key='_DEL_STEP_')

step_panel = [
    [sg.Text('Steps:')],
    [steps_listbox],
    [sg.Text('\nCreate new step:\n')],
    [sg.Text('Step\'s Question:')],
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

def getCommandIndex() -> int:
    indexes = commands_listbox.get_indexes()
    if len(indexes) == 0:
        return -1
    else:
        return indexes[0]
    
def getStepIndex() -> int:
    indexes = steps_listbox.get_indexes()
    if len(indexes) == 0:
        return -1
    else:
        return indexes[0]

def hasCommand(bot:Bot, command_name:str) -> bool:
    for cmd in bot.commands:
        if cmd.name == command_name:
            return True
    return False



currentCommandIndex : int = -1
currentStepIndex : int = -1

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
            error_empty('name')
        elif(len(fieldSucMes) == 0):
            error_empty('success message')
        elif(hasCommand(bot,fieldName)):
            sg.popup_ok('Command names must be unique',title='Error')
        else:
            bot.commands.append(Command(fieldName,fieldSucMes))
            commands_list.append(fieldName)
            commands_listbox.update(commands_list)
    elif event == add_step_button.key:
        fieldQuestion = step_question.get()
        fieldMedia = step_media.get()
        if(len(fieldQuestion) == 0):
            error_empty('question')
        elif(fieldMedia == None or len(fieldMedia) == 0):
            error_empty('media type')
        elif valid_media_type(fieldMedia) == -1 :
            sg.popup_ok('Unknown Media Type',title='Error')
        else:
            step = Step(fieldQuestion,valid_media_type(fieldMedia))
            bot.commands[currentCommandIndex].steps.append(step)
            steps_list.append(fieldQuestion)
            steps_listbox.update(steps_list)
    elif event == delete_command_button.key:
        if(currentCommandIndex != -1):
            bot.commands.pop(currentCommandIndex)
            commands_list.pop(currentCommandIndex)
            commands_listbox.update(commands_list)
            currentCommandIndex = getCommandIndex()
    elif event == delete_step_button.key:
        if(currentStepIndex != -1):
            bot.commands[currentCommandIndex].steps.pop(currentStepIndex)
            steps_list.pop(currentStepIndex)
            steps_listbox.update(commands_list)
            currentStepIndex = getStepIndex()
    elif event == commands_listbox.key:
        currentCommandIndex = getCommandIndex()
        if currentCommandIndex != -1:
            steps_list.clear()
            for step in bot.commands[currentCommandIndex].steps:
                steps_list.append(step.question)
            steps_listbox.update(steps_list)
    elif event == steps_listbox.key:
        currentStepIndex = getStepIndex()
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