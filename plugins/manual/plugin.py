import sys, os
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from botmakerapi import TelegramClient

class Plugin:

    def __init__(self, name:str, commands: list[str]):
        self.name = name
        self.commands = commands

def discoverPlugins(path: Path) -> list[Plugin]:
    plugins = []
    for entry in os.listdir(path):
        entryPath = path.joinpath(entry)
        if entryPath.is_dir():
            rootFilePath = entryPath.joinpath('plugin.py')
            if rootFilePath.exists():
                modName = 'plugin'
                spec = spec_from_file_location(modName,rootFilePath)
                if(spec == None):
                    continue
                mod = module_from_spec(spec)
                sys.modules[modName] = mod
                if(spec.loader == None):
                    continue
                spec.loader.exec_module(mod)
                if(mod.handlers != None):
                    commandNames = list(dict.keys(mod.handlers))
                    plugins.append(Plugin(entry,commandNames))
    return plugins


MANUAL_PLUGIN_DESC = 'مجموعه دستورات'
PLUGINS_DIR = Path('plugins')

man = ''

def __plugin_init__():
    
    global man
    
    for plugin in discoverPlugins(PLUGINS_DIR):
        
        man += MANUAL_PLUGIN_DESC
        man += ' '
        man += plugin.name
        man += '\n'
        
        for cmd in plugin.commands:
            if cmd != '__plugin_init__':
                man += '/'
                man += cmd
                man += '\n'               

        man += '\n'

async def manualHandler(client:TelegramClient, _:str):
    await client.send(man)

handlers = {
    'manual' : manualHandler,
    '__plugin_init__': __plugin_init__,
}