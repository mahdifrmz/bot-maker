### Basic in-memory ticket system ###

lastGenId = 0

def genId() -> int:
    global lastGenId

    lastGenId += 1
    return lastGenId


class Message:
    def __init__(self, content:str, authorIsUser:bool) -> None:
       self.content = content
       self.authorIsUser = authorIsUser

class Ticket:
    
    def __init__(self, userId:int, title:str, firstMessage : Message) -> None:
        self.title = title
        self.userId = userId
        self.id = genId()
        self.messages = [firstMessage]
        self.isOpen = True

ticketsMap : dict[int,Ticket] = {}

def ticket_log(data:str):
    print(data)
### User API ###

async def ticket_new(userId : int, title : str, content : str) -> int:
    mesg = Message(content, True)
    ticket = Ticket(userId, title, mesg)
    ticketsMap[ticket.id] = ticket
    # TODO: INFORM OPERATOR
    ticket_log('|{}|<{}>| -> {}'.format(ticket.id,ticket.title,mesg.content))
    return ticket.id

async def ticket_list(userId : int) -> list[tuple[bool,str]]:
    ticketList = []
    for ticketId in ticketsMap:
        ticket = ticketsMap[ticketId]
        if(userId == ticket.userId):
            ticketList.append((ticket.isOpen,ticket.title))
    return ticketList

async def ticket_status(ticketId : int) -> bool:
    ticket = ticketsMap[ticketId]
    return ticket.isOpen

async def ticket_resume(ticketId : int, content : str):
    mesg = Message(content,True)
    ticket = ticketsMap[ticketId]
    ticket.messages.append(mesg)
    ticket_log('|{}|<{}>| -> {}'.format(ticket.id,ticket.title,mesg.content))
    # TODO: INFORM OPERATOR

async def ticket_reopen(ticketId : int):
    ticket = ticketsMap[ticketId]
    ticket.isOpen = True
    ticket_log('|{}|<{}>| -> OPEN'.format(ticket.id,ticket.title))

async def ticket_close(ticketId : int):
    ticket = ticketsMap[ticketId]
    ticket.isOpen = False
    ticket_log('|{}|<{}>| -> CLOSE'.format(ticket.id,ticket.title))


### Plugin ###

from botmakerapi import TelegramClient, TelegramMessage
from pathlib import Path

TICKET_MESSAGE_ENTER_TITLE = 'عنوان تیکت را وارد کنید.'
TICKET_MESSAGE_ENTER_CONTENT = 'توضیح مشکلی که در حین استفاده از ربات  به آن برخوردید را وارد کنید'
TICKET_MESSAGE_OK = 'تیکت شما ثبت شد. همکاران ما در اسرع وقت اقدام به پاسخگویی می‌کنند. با تشکر.'
TICKET_ERROR_MEDIA = 'آیتم شما باید یک نوشته باشد'
TICKET_ERROR_REPLY = 'این دستور باید به یکی از پیام های تیکت ریپلای شود.'

TICKET_HELP = ''' تیکت ابزار ارتباط با پیشتیبانی ربات می‌باشد
از دستور /ticket_new برای ایجاد تیکت جدید استفاده کنید.
از دستور /ticket_list برای مشاهده وضعیت کل تیکت هایی که ایجاد کرده اید استفاده کنید

برای استفاده از باقی دستورها لازم است تا آنها را به یکی از پیام های تیکت ریپلای کنید.

از دستور /ticket_resume برای فرستادن مجدد پیام استفاده کنید.
از دستور /ticket_status برای مشاهده وضعیت تیکت استفاده کنید.
از دستور /ticket_close برای بستن تیکت استفاده کنید.
از دستور /ticket_reopen برای باز کردن مجدد تیکت استفاده کنید.
'''

messageTicketMap :dict[int,int] = {}

async def recvString(client:TelegramClient) -> tuple[int,str]:
    while(True):
            item = await client.receive()
            if(item.text == None or item.text == ''):
                await client.send(TICKET_ERROR_MEDIA)
                continue
            return (item.id,item.text)
    
async def ticketNewHandler(client:TelegramClient, _:str):
    await client.send(TICKET_MESSAGE_ENTER_TITLE)
    (titleId, title) = await recvString(client)
    await client.send(TICKET_MESSAGE_ENTER_CONTENT)
    (contentId, content) = await recvString(client)
    ticketId = await ticket_new(client.chatId,title,content)
    messageTicketMap[contentId] = ticketId
    await client.send(TICKET_MESSAGE_OK)

async def ticketListHandler(client:TelegramClient, _:str):
    mesg = ''
    for (status,title) in await ticket_list(client.chatId):
        mesg += title + '\n'
        mesg += 'status: ' + ('open' if status else 'closed') + '\n\n'
    await client.send(mesg)

async def ticketResumeHandler(client:TelegramClient, _:str):
    if(client.replyMessageId == 0):
        return await client.send(TICKET_ERROR_REPLY)
    ticketId = messageTicketMap[client.replyMessageId]
    await client.send(TICKET_MESSAGE_ENTER_CONTENT)
    (contentId, content) = await recvString(client)
    await ticket_resume(ticketId, content)
    messageTicketMap[contentId] = ticketId
    await client.send(TICKET_MESSAGE_OK)

async def ticketStatusHandler(client:TelegramClient, _:str):
    if(client.replyMessageId == 0):
        return await client.send(TICKET_ERROR_REPLY)
    ticketId = messageTicketMap[client.replyMessageId]
    status = 'OPEN' if ticket_status(ticketId) else 'CLOSED'
    await client.send(status)

async def ticketReopenHandler(client:TelegramClient, _:str):
    if(client.replyMessageId == 0):
        return await client.send(TICKET_ERROR_REPLY)
    ticketId = messageTicketMap[client.replyMessageId]
    await ticket_reopen(ticketId)

async def ticketCloseHandler(client:TelegramClient, _:str):
    if(client.replyMessageId == 0):
        return await client.send(TICKET_ERROR_REPLY)
    ticketId = messageTicketMap[client.replyMessageId]
    await ticket_close(ticketId)

async def ticketHelpHandler(client:TelegramClient, _:str):
    await client.send(TICKET_HELP)

def __plugin_init__():
    pass


handlers = {
    'ticket_new' : ticketNewHandler,
    'ticket_list' : ticketListHandler,
    'ticket_status' : ticketStatusHandler,
    'ticket_resume' : ticketResumeHandler,
    'ticket_reopen' : ticketReopenHandler,
    'ticket_close' : ticketCloseHandler,
    'ticket_help' : ticketHelpHandler,
    '__plugin_init__' : __plugin_init__,
}