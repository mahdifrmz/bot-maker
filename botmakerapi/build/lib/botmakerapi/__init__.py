from telegram import Bot, Message
from asyncio import Queue
from pathlib import Path

class TelegramMessage:

    def __init__(self, message: Message):
        self.text = message.text
        self.photo = message.photo
        self.audio = message.audio
        self.video = message.video
        self.document = message.document
        self.id = message.id

class TelegramClient:
    
    def __init__(self, bot:Bot, queue: Queue, chatId:int, messageId:int, replyMessageId:int):
        self.bot = bot
        self.queue = queue
        self.chatId = chatId
        self.messageId = messageId
        self.replyMessageId = replyMessageId

    async def send(self, message: str):
        await self.bot.send_message(chat_id=self.chatId, text=message)

    async def sendFile(self, path: str):
        await self.bot.send_document(chat_id=self.chatId, document=Path(path))

    async def receive(self) -> TelegramMessage:
        return await self.queue.get()