# imports

import logging
import uuid
import os
from telegram import Update , Video, Audio, Voice, PhotoSize, Bot, Document, Message
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,filters
from pathlib import Path
import aiofiles
from mimetypes import guess_extension
from asyncio import Queue, create_task, Task
from botmakerapi import TelegramClient, TelegramMessage
import plugin1.plugin as bmp1

plugins = [
    bmp1.handlers
]

# constants

MESSAGE_TYPE_TEXT = 1
MESSAGE_TYPE_IMAGE = 2
MESSAGE_TYPE_AUDIO = 3
MESSAGE_TYPE_VIDEO = 4
MESSAGE_TYPE_DOC = 5

DEFAULT_EXTENSION = 'data'

COMMAND_HELP = 'help'
COMMAND_START = 'start'
COMMAND_CANCEL = 'cancel'

# configs

BOT_TOKEN = '6107216509:AAGSIEC4W0ReW-pnThSqNwh823O5Hya5shk'
STORAGE_ROOT = './storage'

RESPONSE_CANCEL = 'Ok, anything else?'
RESPONSE_HELP = '''

This bot has the following commands:

/foo : foo
/bar : bar

/help : shows this help
/cancel : cancels
'''

RESPONSE_INVALID = 'Sorry, that\'s an invalid input'
RESPONSE_START = 'Welcome to the Sample Bot!\nUse /help to get the manual for using this bot'

# commands

COMMAND1_SUCCESS = 'successfully fooed'
COMMAND1_NAME = 'foo'

COMMAND2_SUCCESS = 'successfully barred'
COMMAND2_NAME = 'bar'

COMMAND3_NAME = 'qin'

# steps

USERSTATE_CMD1_STEP1 = 231244
USERSTATE_CMD1_STEP1_INFORM = 'Name the foo'

USERSTATE_CMD1_STEP2 = 20932489
USERSTATE_CMD1_STEP2_INFORM = 'upload a video describing the foo'

USERSTATE_CMD1_STEP3 = 99231244
USERSTATE_CMD1_STEP3_INFORM = 'send the sound your foo makes'

USERSTATE_CMD2_STEP1 = 4354354
USERSTATE_CMD2_STEP1_INFORM = 'explain the bar'

USERSTATE_CMD2_STEP2 = 12324235
USERSTATE_CMD2_STEP2_INFORM = 'send the bar code'

# utils

class UserState:
    
    def __init__(self):
        self.count = 0
        self.step = 0
        self.dirId = ''
        self.queue : Queue | None = Queue()
        self.task : Task | None = None

    async def sendToQueue(self,message:TelegramMessage):
        if(self.queue):
            await self.queue.put(message)

    def cancelTask(self):
        if(self.task):
            self.task.cancel()

class StateManager:

    states : dict[int,UserState] = {}

    @staticmethod
    def get(id:int) -> UserState | None:
        return StateManager.states.get(id)

    @staticmethod
    def create(id:int) -> UserState:
        state = UserState()
        StateManager.states[id] = state
        return state
    
    @staticmethod
    def remove(id:int):
        del StateManager.states[id]

class Storage:

    root = Path(STORAGE_ROOT)

    @staticmethod
    def generateUuid() -> str:
        return uuid.uuid4().hex
    
    @staticmethod
    def rmdir(directory : Path):
        directory = Path(directory)
        for item in directory.iterdir():
            if item.is_dir():
                Storage.rmdir(item)
            else:
                item.unlink()
        directory.rmdir()
    
    @staticmethod
    def remove(dirId:str):
        path = Storage.dirPath(dirId)
        Storage.rmdir(path)

    @staticmethod
    def create() -> str:
        dirId = Storage.generateUuid()
        path = Storage.dirPath(dirId)
        os.mkdir(path)
        return dirId
    
    @staticmethod
    def dirPath(dirId:str) -> Path:
        return Storage.root.joinpath(dirId)
    
    @staticmethod
    def path(dirId:str,num:int,ext:str) -> Path:
        dir = Storage.dirPath(dirId)
        file = str(num) + ext
        return dir.joinpath(file)

async def saveText(state:UserState, text: str):
    path = Storage.path(state.dirId, state.count, '.txt')
    async with aiofiles.open(path, mode='w') as f:
        await f.write(text)

def translateMIME(mime_type:str) -> str | None:
    return guess_extension(mime_type)

async def recvFile(path:Path, file: Audio | Video | Voice | PhotoSize):
    telegramFile = await file.get_file()
    await telegramFile.download_to_drive(path)

async def recvMedia(state:UserState, file: Audio | Video | Voice):
    ext = translateMIME(file.mime_type) or DEFAULT_EXTENSION if file.mime_type else DEFAULT_EXTENSION
    path = Storage.path(state.dirId, state.count, ext)
    await recvFile(path, file)

async def recvPhoto(state:UserState, file: PhotoSize):
    path = Storage.path(state.dirId, state.count, '.jpg')
    await recvFile(path, file)
    
def getChatId(update: Update) -> int:
    chat = update.effective_chat
    return exit(1) if chat == None else chat.id

def installPluginHandlers(application:Application):
    
    commandNames : set[str] = set()
    
    for handlerMap in plugins:
        for commandName in handlerMap:
            # command names must be unique
            if(commandName in commandNames):
                raise Exception('Command Name ' + commandName + 'previously registered!')
            commandNames.add(commandName)
            # create handler
            async def handleCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):    
                id = getChatId(update)
                state = StateManager.get(id)
                if(state == None):
                    state = StateManager.create(id)
                    state.step = -1
                    state.queue = Queue()
                    client = TelegramClient(context.bot, state.queue, id)
                    text = (update.message.text or '') if update.message else ''
                    async def handler():
                        await handlerMap[commandName](client,text)
                        StateManager.remove(id)
                    state.task = create_task(handler())
                else:
                    await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
            # install handler
            command_handler = CommandHandler(commandName, handleCommand)
            application.add_handler(command_handler)

# basic handlers

async def handleCancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = getChatId(update)
    state = StateManager.get(id)
    if(state):
        state.cancelTask()
        Storage.remove(state.dirId)
        StateManager.remove(id)
        await context.bot.send_message(chat_id=id, text=RESPONSE_CANCEL)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = getChatId(update)
    state = StateManager.get(id)
    if(state == None):
        await context.bot.send_message(chat_id=id, text=RESPONSE_START)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleHelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = getChatId(update)
    state = StateManager.get(id)
    if(state == None):
        await context.bot.send_message(chat_id=id, text=RESPONSE_HELP)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

# command handlers

async def handleCommand1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = getChatId(update)
    state = StateManager.get(id)
    if(state == None):
        state = StateManager.create(id)
        state.step = USERSTATE_CMD1_STEP1
        state.count += 1
        state.dirId = Storage.create()
        await context.bot.send_message(chat_id=id, text=USERSTATE_CMD1_STEP1_INFORM)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleCommand2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = getChatId(update)
    state = StateManager.get(id)
    if(state == None):
        state = StateManager.create(id)
        state.step = USERSTATE_CMD2_STEP1
        state.count += 1
        state.dirId = Storage.create()
        await context.bot.send_message(chat_id=id, text=USERSTATE_CMD2_STEP1_INFORM)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

# message handler

async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if(message == None):
        return
    id = getChatId(update)
    state = StateManager.get(id)
    if(state == None):
        return await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    if(state.step == -1):
        return await state.sendToQueue(TelegramMessage(message))
    # COMMAND 1
    elif (state.step == USERSTATE_CMD1_STEP1):
        if(message.text):
            await saveText(state,message.text)
            state.count += 1
            state.step = USERSTATE_CMD1_STEP2
            await context.bot.send_message(chat_id=id, text=USERSTATE_CMD1_STEP2_INFORM)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    elif (state.step == USERSTATE_CMD1_STEP2):
        try:
            if(message.video):
                await recvMedia(state,message.video)
                state.count += 1
                state.step = USERSTATE_CMD1_STEP3
                await context.bot.send_message(chat_id=id, text=USERSTATE_CMD1_STEP3_INFORM)
            else:
                await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
        except:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    elif (state.step == USERSTATE_CMD1_STEP3):
        try:
            if(message.voice):
                await recvMedia(state,message.voice)
                StateManager.remove(id)
                await context.bot.send_message(chat_id=id, text=COMMAND1_SUCCESS)
            else:
                await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
        except:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    # COMMAND 2
    elif (state.step == USERSTATE_CMD2_STEP1):
        if(message.text):
            await saveText(state, message.text)
            state.count += 1
            state.step = USERSTATE_CMD2_STEP2
            await context.bot.send_message(chat_id=id, text=USERSTATE_CMD2_STEP2_INFORM)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    elif (state.step == USERSTATE_CMD2_STEP2):
        if(message.text):
            await saveText(state,message.text)
            StateManager.remove(id)
            await context.bot.send_message(chat_id=id, text=COMMAND2_SUCCESS)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

# main

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == "__main__":

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    installPluginHandlers(application)
        
    message_handler = MessageHandler(~filters.COMMAND, handleMessage)
    application.add_handler(message_handler)

    command1_handler = CommandHandler(COMMAND1_NAME, handleCommand1)
    application.add_handler(command1_handler)

    command2_handler = CommandHandler(COMMAND2_NAME, handleCommand2)
    application.add_handler(command2_handler)

    help_handler = CommandHandler(COMMAND_HELP, handleHelp)
    application.add_handler(help_handler)

    cancel_handler = CommandHandler(COMMAND_CANCEL, handleCancel)
    application.add_handler(cancel_handler)

    start_handler = CommandHandler(COMMAND_START, handleStart)
    application.add_handler(start_handler)

    application.run_polling()