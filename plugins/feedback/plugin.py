from botmakerapi import TelegramClient
from pathlib import Path
import uuid, os

ENTER_MESSAGE = 'نظر خود را راجع به ربات وارد کنید'
OK_MESSAGE = 'نظر شما ثبت شد. با تشکر فراوان.'
MEDIA_ERROR = 'آیتم شما باید یک نوشته باشد'

FEEDBACK_DIR_PATH = 'plugins/feedback/feedbacks/'

async def feedbackHandler(client:TelegramClient, _:str):
    await client.send(ENTER_MESSAGE)
    message = ''
    while(True):
        item = await client.receive()
        if(item.text == None or item.text == ''):
            await client.send(MEDIA_ERROR)
            continue
        message = item.text
        break
    fileName = uuid.uuid4().hex + '.txt'
    filePath = Path(FEEDBACK_DIR_PATH).joinpath(fileName)
    with open(filePath, 'w') as file:
        file.write(message)
    await client.send(OK_MESSAGE)

def __plugin_init__():
    if not Path(FEEDBACK_DIR_PATH).is_dir():
        os.mkdir(FEEDBACK_DIR_PATH)

handlers = {
    'feedback' : feedbackHandler,
    '__plugin_init__': __plugin_init__,
}