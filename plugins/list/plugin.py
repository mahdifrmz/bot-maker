from botmakerapi import TelegramClient

ENTER_MESSAGE = 'آیتم مد نظرتان را در یک خط بنویسید'
MULTILINE_ERROR = 'آیتم شما باید یک خط باشد'
MEDIA_ERROR = 'آیتم شما باید یک نوشته باشد'
SUCCESS_MESSAGE = 'آیتم به لیست اضافه شد'

async def appendHandler(client:TelegramClient, text:str):
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
    with open('list.txt','+a') as list:
        list.write(line)
        list.write('\n')
    await client.send(SUCCESS_MESSAGE)

handlers = {
    'addtolist' : appendHandler
}