import PySimpleGUI as sg

from codegen import Bot, Plugin, Command, Step
from general import EVENT_HELP_BUTTON, help_button, next_button,back_button, WINDOW_TITLE, error_empty, EVENT_NEXT_BUTTON, EVENT_BACK_BUTTON
from codegen import BotMakerContext
from help import HELP_COMMANDS, show_help

MEDIA_TYPES = ['Text','Image','Audio','Video','Document']

def valid_media_type(name:str) -> int:
    i = 0
    for mt in MEDIA_TYPES:
        i += 1
        if mt == name:
            return i
    return -1

def hasCommand(bot:Bot, plugins:list[Plugin], command_name:str) -> bool:
    for cmd in bot.commands:
        if cmd.name == command_name:
            return True
    for plugin in plugins:
        if command_name in plugin.commands:
            return True
    return False

def runView(context:BotMakerContext) -> bool:

    commandsList = []
    commands_listbox = sg.Listbox(commandsList, enable_events=True, key='_LIST_COMMAND_', size=(45,10))
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
        [back_button(),add_command_button,delete_command_button,next_button()],
        [help_button()]

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

    currentCommandIndex : int = -1
    currentStepIndex : int = -1

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

    for cmd in context.bot.commands:
        commandsList.append(cmd.name)

    winrsl = True

    while True:
        ev = window.read()
        if ev == None:
            continue
        event, values = ev
        if event == EVENT_NEXT_BUTTON:
            break
        elif event == EVENT_BACK_BUTTON:
            winrsl = False
            break
        elif event == add_command_button.key:
            fieldName = command_name.get()
            fieldSucMes = command_success_message.get()
            if(len(fieldName) == 0):
                error_empty('name')
            elif(len(fieldSucMes) == 0):
                error_empty('success message')
            elif(hasCommand(context.bot, context.addedPlugins(), fieldName)):
                sg.popup_ok('Command names must be unique',title='Error')
            else:
                context.bot.commands.append(Command(fieldName,fieldSucMes))
                commandsList.append(fieldName)
                commands_listbox.update(commandsList)
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
                context.bot.commands[currentCommandIndex].steps.append(step)
                steps_list.append(fieldQuestion)
                steps_listbox.update(steps_list)
        elif event == delete_command_button.key:
            if(currentCommandIndex != -1):
                context.bot.commands.pop(currentCommandIndex)
                commandsList.pop(currentCommandIndex)
                commands_listbox.update(commandsList)
                currentCommandIndex = getCommandIndex()
        elif event == delete_step_button.key:
            if(currentStepIndex != -1):
                context.bot.commands[currentCommandIndex].steps.pop(currentStepIndex)
                steps_list.pop(currentStepIndex)
                steps_listbox.update(commandsList)
                currentStepIndex = getStepIndex()
        elif event == commands_listbox.key:
            currentCommandIndex = getCommandIndex()
            if currentCommandIndex != -1:
                steps_list.clear()
                for step in context.bot.commands[currentCommandIndex].steps:
                    steps_list.append(step.question)
                steps_listbox.update(steps_list)
        elif event == steps_listbox.key:
            currentStepIndex = getStepIndex()
        elif event == sg.WIN_CLOSED:
            exit(0)
        elif event == EVENT_HELP_BUTTON:
            show_help(HELP_COMMANDS)


    window.close()
    return winrsl