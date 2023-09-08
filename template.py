import logging
import uuid
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler,filters
from pathlib import Path
import aiofiles

BOT_TOKEN = '6107216509:AAGSIEC4W0ReW-pnThSqNwh823O5Hya5shk'
STORAGE_ROOT = './storage'

MESSAGE_TYPE_TEXT = 1
MESSAGE_TYPE_IMAGE = 2
MESSAGE_TYPE_AUDIO = 3
MESSAGE_TYPE_VIDEO = 4
MESSAGE_TYPE_DOC = 5

RESPONSE_CANCEL = 'Ok, anything else?'
RESPONSE_HELP = '''

This bot has the following commands:

/foo : foo
/bar : bar

/help : shows this help
/cancel : cancels
'''

RESPONSE_INVALID = 'Sorry, that\'s and invalid input'
RESPONSE_START = 'Welcome to the Sample Bot!\nUse /help to get the manual for using this bot'

COMMAND1_SUCCESS = 'successfully fooed'
COMMAND1_NAME = 'foo'

COMMAND2_SUCCESS = 'successfully barred'
COMMAND2_NAME = 'bar'

USERSTATE_CMD1_STEP1 = 231244
USERSTATE_CMD1_STEP1_INFORM = 'Name the foo'
USERSTATE_CMD1_STEP1_TYPE = MESSAGE_TYPE_TEXT

USERSTATE_CMD1_STEP2 = 20932489
USERSTATE_CMD1_STEP2_INFORM = 'upload a video describing the foo'
USERSTATE_CMD1_STEP2_TYPE = MESSAGE_TYPE_VIDEO

USERSTATE_CMD1_STEP3 = 231244
USERSTATE_CMD1_STEP3_INFORM = 'send the sound your foo makes'
USERSTATE_CMD1_STEP3_TYPE = MESSAGE_TYPE_AUDIO

USERSTATE_CMD2_STEP1 = 4354354
USERSTATE_CMD2_STEP1_INFORM = 'explain the bar'
USERSTATE_CMD2_STEP1_TYPE = MESSAGE_TYPE_TEXT

USERSTATE_CMD2_STEP2 = 12324235
USERSTATE_CMD2_STEP2_INFORM = 'send the bar code'
USERSTATE_CMD2_STEP2_TYPE = MESSAGE_TYPE_TEXT

class UserState:
    
    def __init__(self):
        self.count = 0
        self.step = 0
        self.dirId = None


class StateManager:

    states : dict[int,UserState] = {}

    def get(id) -> UserState:
        return StateManager.states[id]

    def create(id:int) -> UserState:
        state = UserState()
        StateManager.states[id] = state
        return state

    def remove(id:int):
        del StateManager.states[id]

class Storage:

    root = Path(STORAGE_ROOT)

    def generateUuid() -> str:
        return uuid.uuid4().hex

    def rmdir(directory):
        directory = Path(directory)
        for item in directory.iterdir():
            if item.is_dir():
                Storage.rmdir(item)
            else:
                item.unlink()
        directory.rmdir()
    
    def remove(dirId:str):
        path = Storage.dirPath(dirId)
        Storage.rmdir(path)

    async def create() -> str:
        dirId = Storage.generateUuid()
        path = Storage.dirPath(dirId)
        os.mkdir(path)
        return dirId
    
    def dirPath(dirId:str) -> Path:
        return Storage.root.joinpath(dirId)
    
    def objName(num:int,filename:str) -> str:
        dotIndex = filename.rfind('.')
        if(dotIndex > -1):
            filename = filename[dotIndex,]
        else:
            filename = ''
        return str(num).join([filename])
        
    def path(dirId:str,num:int,filename:str) -> Path:
        dir = Storage.dirPath(dirId)
        file = Storage.objName(num,filename)
        return dir.joinpath(file)

async def recvFile(state:UserState, file):
    if(type(file) == type('')):
        path = Storage.path(state.dirId, state.count, None)
        async with aiofiles.open(path, mode='w') as f:
            await f.write(file)
    else:
        path = Storage.path(state.dirId, state.count, file.file_name)
        telegramFile = await file.get_file(file)
        await telegramFile.download_to_drive(path)

async def handleCommand1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    if(state == None):
        state = StateManager.create(id)
        state.count += 1
        state.step = USERSTATE_CMD1_STEP1
        state.dirId = Storage.create()
        await context.bot.send_message(chat_id=id, text=USERSTATE_CMD1_STEP1_INFORM)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleCommand2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    if(state == None):
        state = StateManager.create(id)
        state.count += 1
        state.step = USERSTATE_CMD2_STEP1
        state.dirId = Storage.create()
        await context.bot.send_message(chat_id=id, text=USERSTATE_CMD2_STEP1_INFORM)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    if(state == None):
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    # COMMAND 1
    elif (state.step == USERSTATE_CMD1_STEP1):
        if(update.message.text):
            state.count += 1
            recvFile(state,update.message.text)
            state.step = USERSTATE_CMD1_STEP2
            await context.bot.send_message(chat_id=id, text=USERSTATE_CMD1_STEP2_INFORM)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    elif (state.step == USERSTATE_CMD1_STEP2):
        if(update.message.video):
            state.count += 1
            recvFile(state,update.message.video)
            state.step = USERSTATE_CMD1_STEP3
            await context.bot.send_message(chat_id=id, text=USERSTATE_CMD1_STEP3_INFORM)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    elif (state.step == USERSTATE_CMD1_STEP3):
        if(update.message.video):
            StateManager.remove(id)
            await context.bot.send_message(chat_id=id, text=COMMAND1_SUCCESS)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    # COMMAND 2
    elif (state.step == USERSTATE_CMD2_STEP1):
        if(update.message.text):
            state.count += 1
            recvFile(state,update.message.text)
            state.step = USERSTATE_CMD2_STEP2
            await context.bot.send_message(chat_id=id, text=USERSTATE_CMD2_STEP2_INFORM)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    elif (state.step == USERSTATE_CMD2_STEP2):
        if(update.message.video):
            StateManager.remove(id)
            await context.bot.send_message(chat_id=id, text=COMMAND2_SUCCESS)
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)
    

async def handleCancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    if(state):
        Storage.remove(state.dirId)
        StateManager.remove(id)
        await context.bot.send_message(chat_id=id, text=RESPONSE_CANCEL)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    if(state == None):
        await context.bot.send_message(chat_id=id, text=RESPONSE_START)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

async def handleHelp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    if(state == None):
        await context.bot.send_message(chat_id=id, text=RESPONSE_HELP)
    else:
        await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == "__main__":

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    message_handler = MessageHandler(~filters.COMMAND, handleMessage)
    application.add_handler(message_handler)

    command1_handler = CommandHandler(COMMAND1_NAME, handleCommand1)
    application.add_handler(command1_handler)

    command2_handler = CommandHandler(COMMAND2_NAME, handleCommand2)
    application.add_handler(command2_handler)

    application.run_polling()