import asyncio
import ImageBoard.dvach as dvach
from queue import Queue
from pyrogram.types import InputMediaPhoto, InputMediaVideo

message_queue = Queue()

from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)

telegram_client = Client("my_bot")
InputMediaVideo("video.mp4", caption="video caption")

async def start_bot():
    telegram_client.run(dvach.Queue)
    asyncio.futures. message_queue.put(dvach.update_threads())
    while True:
        if message_queue.not_empty:
            message = message_queue.get()
            if len(message["media"]) == 1:
                telegram_client.send_video()
            elif len(message["media"]) > 1:
                telegram_client.send_media_group()



asyncio.run(start_bot())