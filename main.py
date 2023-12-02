import PySimpleGUI as sg
import os
import shutil
from pathlib import Path
from codegen import Bot, Generator, discoverPlugins

import ui.welcome as welcomeView
import ui.cred as credentialsView
import ui.plugin as pluginsView
import ui.commands as commandsView
import ui.metadata as metadataView
import ui.getpath as getPathView
import ui.end as endView

STORAGE_PATH = 'storage'

bot = Bot()
botOutput = [
    '', # Path
    '' # Name
]
bot.storage_root = STORAGE_PATH

plugins = discoverPlugins(Path('plugins'))
plugin_checks = len(plugins) * [False]
plugin_names = list(map(lambda plugin : plugin.name, plugins))
plugin_chosen = []

welcomeView.runView()

credentialsView.runView(bot)

pluginsView.runView(plugin_names,plugin_checks)
for i in range(len(plugins)):
    if plugin_checks[i]:
        plugin_chosen.append(plugins[i])

commandsView.runView(bot,plugins)

metadataView.runView(bot)

getPathView.runView(botOutput)

src = Generator().generate(bot,plugins)

path = Path.joinpath(Path(botOutput[0]), botOutput[1])
storage_path = Path.joinpath(path, STORAGE_PATH)
src_path = Path.joinpath(path, 'bot.py')
plugins_path = Path.joinpath(path, 'plugins')

os.mkdir(path)
os.mkdir(storage_path)
open(src_path,'w').write(src)

for plugin in plugins:
    print('plugin:',plugin.name)
    print(
        Path('plugins').joinpath(plugin.name),
        plugins_path.joinpath(plugin.name)
    )
    shutil.copytree(
        Path('plugins').joinpath(plugin.name),
        plugins_path.joinpath(plugin.name)
    )

endView.runView()