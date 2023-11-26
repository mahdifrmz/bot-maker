from botmakerapi import TelegramClient
from pathlib import Path
import uuid, os

SUB_MESSAGE_DONE = "You successfully subscribed to the bot"
SUB_MESSAGE_UNDONE = "You ended your subscription"
SUB_ERROR_ALREADY_IN_LIST = "You are already a subscriber"
SUB_ERROR_NOT_IN_LIST = "You are not a subscriber"

SUB_FILE_PATH = 'plugins/subscription/subscriptions.txt'

def loadList() -> list[str]:
    with open(SUB_FILE_PATH,'r') as list:
        return [l.strip() for l in list.readlines()]

def storeList(entries: list[str]):
    with open(SUB_FILE_PATH,'w') as list:
        for item in entries:
                list.write(item)
                list.write('\n')

async def subHandler(client:TelegramClient, _:str):
    subs = loadList()
    id = str(client.chatId)
    if(id in subs):
        await client.send(SUB_ERROR_ALREADY_IN_LIST) 
    else:
        subs.append(id)
        storeList(subs)
        await client.send(SUB_MESSAGE_DONE)
         
async def unsubHandler(client:TelegramClient, _:str):
    subs = loadList()
    id = str(client.chatId)
    if(id in subs):
        subs.remove(id)
        storeList(subs)
        await client.send(SUB_MESSAGE_UNDONE)
    else:
        await client.send(SUB_ERROR_NOT_IN_LIST)
         
def __plugin_init__():
    if not Path(SUB_FILE_PATH).is_file():
        open(SUB_FILE_PATH,'x')

handlers = {
    'subscribe' : subHandler,
    'unsubscribe' : unsubHandler,
    '__plugin_init__': __plugin_init__,
}