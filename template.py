import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

RESPONSE_CANCEL = ''
RESPONSE_HELP = ''
RESPONSE_INVALID = ''
RESPONSE_START = ''

USERSTATE_CMD1_STEP1 = 231244
USERSTATE_CMD1_STEP1_INFORM = ''

USERSTATE_CMD1_STEP2 = 20932489
USERSTATE_CMD1_STEP2_INFORM = ''

USERSTATE_CMD1_STEP3 = 231244
USERSTATE_CMD1_STEP3_INFORM = ''

USERSTATE_CMD2_STEP1 = 4354354
USERSTATE_CMD2_STEP1_INFORM = ''

USERSTATE_CMD2_STEP2 = 12324235
USERSTATE_CMD2_STEP2_INFORM = ''

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
    
    def remove(dirId:str):
        pass
    
    def create() -> int:
        pass
    
    def path(dirId:str,num:int,filename:str) -> str:
        pass

async def recvFile(state:UserState, file):
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
    elif (state.step == USERSTATE_CMD1_STEP1):
        if(update.message.video):
            pass
        else:
            await context.bot.send_message(chat_id=id, text=RESPONSE_INVALID)


async def handleCancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    state = StateManager.get(id)
    Storage.remove(state.dirId)
    StateManager.remove(id)
    await context.bot.send_message(chat_id=id, text=RESPONSE_CANCEL)

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
