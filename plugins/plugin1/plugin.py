from botmakerapi import TelegramClient

async def qinHandler(client:TelegramClient, text:str):
    print("MIRROR START")
    await client.send('Mirror mode enabled!\nSend <end> to disable')
    while(True):
        mes = await client.receive()
        print('GOT')
        if(mes.text and len(mes.text) > 0):
            if(mes.text == 'end'):
                await client.send('OK!')
                break
            else:
                await client.send(mes.text)

handlers = {
    'qin' : qinHandler
}