import PySimpleGUI as sg

from ui.general import next_button,back_button,WINDOW_TITLE,EVENT_NEXT_BUTTON,EVENT_BACK_BUTTON

def runView(plugins: list[str], plugin_checks: list[bool]) -> bool:
    panel = []

    for i in range(len(plugins)):
        panel.append([sg.Checkbox(plugins[i],plugin_checks[i])])
    panel.append([back_button(),next_button()])

    window = sg.Window(WINDOW_TITLE, panel)
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
        elif event == sg.WIN_CLOSED:
            exit(0)

    for i in range(len(plugins)):
        plugin_checks[i] = panel[i][0].get()
    
    window.close()
    return winrsl