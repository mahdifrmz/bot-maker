import sys, os
from pathlib import Path
from botmakerapi import TelegramClient

LIBRARY_DIR = 'plugins/library/library/'
NUMBER_ERROR = 'لطفا یک عدد وارد کنید'

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

def getFiles() -> list[str]:
    return list(filter(lambda e : Path(e).is_file(), os.listdir(LIBRARY_DIR)))

def __plugin_init__():
    if not Path(LIBRARY_DIR).is_dir():
        os.mkdir(LIBRARY_DIR)


async def libHandler(client:TelegramClient, _:str):
    files = getFiles()
    files_mesg = stringifyList(files)
    await client.send(files_mesg)
    if(len(files) > 0):
        idx = await readNumber(client)
        await client.sendFile(files[idx-1])

handlers = {
    'library' : libHandler,
    '__plugin_init__': __plugin_init__,
}