from botmakerapi import TelegramClient
from pathlib import Path

ENTER_MESSAGE = 'آیتم مد نظرتان را در یک خط بنویسید'
MULTILINE_ERROR = 'آیتم شما باید یک خط باشد'
MEDIA_ERROR = 'آیتم شما باید یک نوشته باشد'
NUMBER_ERROR = 'لطفا یک عدد وارد کنید'
SUCCESS_MESSAGE = 'آیتم به لیست اضافه شد'
LIST_MESSAGE = 'آیتم های لیست:'
LIST_REMOVE = 'عدد آیتمی که می‌خواهید حذف شود را وارد کنید'

LIST_FILE_PATH = 'plugins/list/list.txt'

async def readNumber(client:TelegramClient) -> int:
    while(True):
        mesg = await client.receive()
        if(mesg.text == None or mesg.text == ''):
            await client.send(NUMBER_ERROR)
            continue
        num = mesg.text
        try:
            num = int(num)
            return num
        except:
            await client.send(NUMBER_ERROR)

async def appendHandler(client:TelegramClient, _:str):
    await client.send(ENTER_MESSAGE)
    line = ''
    while(True):
        item = await client.receive()
        if(item.text == None or item.text == ''):
            await client.send(MEDIA_ERROR)
            continue
        line = item.text
        if(line.find('\n') != -1):
            await client.send(MULTILINE_ERROR)
            continue
        break
    list = loadList()
    list.append(line)
    storeList(list)
    await client.send(SUCCESS_MESSAGE)

def loadList() -> list[str]:
    with open(LIST_FILE_PATH,'r') as list:
        return [l.strip() for l in list.readlines()]

def stringifyList(entries: list[str]):
    if len(entries) > 0:
        mesg = ''
        idx = 0
        for line in entries:
            idx += 1
            mesg += (str(idx) + ') ' + line + '\n')
        return mesg
    else:
        return '<empty>'
    
def storeList(entries: list[str]):
    with open(LIST_FILE_PATH,'w') as list:
        for item in entries:
                list.write(item)
                list.write('\n')

async def removeHandler(client:TelegramClient, _:str):
    entries = loadList()
    await client.send(stringifyList(entries) + '\n' + LIST_REMOVE)
    idx = await readNumber(client)
    entries.pop(idx-1)
    storeList(entries)


async def showHandler(client:TelegramClient, _:str):
    await client.send(stringifyList(loadList()))

def __plugin_init__():
    if not Path(LIST_FILE_PATH).is_file():
        open(LIST_FILE_PATH,'x')

handlers = {
    'list_add' : appendHandler,
    'list_show' : showHandler,
    'list_remove' : removeHandler,
    '__plugin_init__': __plugin_init__,
}