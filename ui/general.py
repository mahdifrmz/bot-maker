import PySimpleGUI as sg

WINDOW_TITLE = 'Bot Maker Wizard'
EVENT_NEXT_BUTTON = '_NEXT_'
EVENT_FINISH_BUTTON = '_FINISH_'
EVENT_BACK_BUTTON = '_BACK_'

def next_button():
    return sg.Button('Next >',key = EVENT_NEXT_BUTTON)

def back_button():
    return sg.Button('< Back',key = EVENT_BACK_BUTTON)

def finish_button():
    return sg.Button('Finish',key = EVENT_FINISH_BUTTON)

def error_empty(field:str):
    sg.popup_ok(field + ' field must be filled',title='Error')
