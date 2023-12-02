import os
import shutil
from pathlib import Path
from codegen import  Generator, discoverPlugins, BotMakerContext

import welcome as welcomeView
import cred as credentialsView
import plugin as pluginsView
import commands as commandsView
import metadata as metadataView
import getpath as getPathView
import end as endView

STORAGE_PATH = 'storage'
PLUGIN_PATH = 'plugins'

context = BotMakerContext(STORAGE_PATH)
context.setPlugins(discoverPlugins(Path(PLUGIN_PATH)))

views = [    
    welcomeView.runView,
    credentialsView.runView,
    pluginsView.runView,
    commandsView.runView,
    metadataView.runView,
    getPathView.runView,
]

view_idx = 0

while(view_idx < len(views)):
    if views[view_idx](context):
        view_idx += 1
    else:
        view_idx -= 1

src = Generator().generate(context.bot, context.addedPlugins())
path = Path.joinpath(Path(context.botOutput[0]), context.botOutput[1])
storage_path = Path.joinpath(path, STORAGE_PATH)
src_path = Path.joinpath(path, 'bot.py')
plugins_path = Path.joinpath(path, 'plugins')

os.mkdir(path)
os.mkdir(storage_path)
open(src_path,'w').write(src)

for plugin in context.addedPlugins():
    print('plugin:',plugin.name)
    print(
        Path('plugins').joinpath(plugin.name),
        plugins_path.joinpath(plugin.name)
    )
    shutil.copytree(
        Path('plugins').joinpath(plugin.name),
        plugins_path.joinpath(plugin.name)
    )

endView.runView(context)