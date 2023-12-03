import PySimpleGUI as sg

def show_help(content:str):
    sg.popup_scrolled(content,title='Help')

HELP_WELCOME ='''
Welcome to Bot Maker application! A no-code tool specialized
for creating Telegram bots only with a few clicks. While the
interface is a user-friendly one, a help button is placed in
every page which will explain to you how you can create your
own bot using this tool.
'''

HELP_CREDENTIALS ='''
In the first page, you should set up the basic parameters of
you bot.
The first field is the token. You should receive it
from BotFather (https://t.me/BotFather).
Next, you should set the /start command text. this text will
be sent to the user everytime they use the /start command.
Next one is the same but for /help command.
'''

HELP_PLUGINS ='''
Each plugin is a set of programmed commands for BotMaker and
you can import them to your bot.
Plugin developers release them as packages which contain a
plugin.py file. You should copy the entire folder into the
plugins directory of BotMaker, so that BotMaker can find them.
There are a handful of default plugins that you can use, so
simply set the check box for every plugin you want to add.
'''

HELP_COMMANDS ='''
This page is the heart of BotMaker platform. Here you define
the core commands of you Teleram bot.
Each command is known to be a sequence of conversation steps
between the user and the bot. In each step the user responds
to a question asked by the bot. Each question has a text and
a required media type which the user's answer should contain.
'''

HELP_METADATA ='''
The first field is the /cancel command message. The /cancel
command is used to abort an on-going conversation to start
a new one.
The error messsage is what the bot sends to user when they
send an invalid input to the bot.
'''

HELP_GETPATH ='''
Simply name the bot and choose the location where BotMaker will
generate the bot's source file in.
'''