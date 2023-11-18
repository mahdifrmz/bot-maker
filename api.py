from telegram import Bot, Message
from asyncio import Queue

class TelegramMessage:

    def __init__(self, message: Message):
        self.text = message.text
        self.photo = message.photo
        self.audio = message.audio
        self.video = message.video
        self.document = message.document

class TelegramClient:
    
    def __init__(self, bot:Bot, queue: Queue, chatId:int):
        self.bot = bot
        self.queue = queue
        self.chatId = chatId

    async def send(self, message: str):
        await self.bot.send_message(chat_id=self.chatId, text=message)

    async def receive(self) -> TelegramMessage:
        return await self.queue.get()