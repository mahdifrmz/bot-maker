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

### User API ###

async def ticket_new(userId : int, title : str, content : str) -> int:
    mesg = Message(content, True)
    ticket = Ticket(userId, title, mesg)
    ticketsMap[ticket.id] = ticket
    # TODO: INFORM OPERATOR
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
    # TODO: INFORM OPERATOR

async def ticket_reopen(ticketId : int):
    ticket = ticketsMap[ticketId]
    ticket.isOpen = True

async def ticket_close(ticketId : int):
    ticket = ticketsMap[ticketId]
    ticket.isOpen = False