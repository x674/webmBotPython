import asyncio
import os
import time

from VideoUtils.webmConverter  import convert_webm_to_mp4,download_file

from pyrogram.types import InputMediaVideo
from pyrogram import Client
from pyrogram.errors import FloodWait,MediaEmpty
from ImageBoard.dvach import message_queue, Message

MEDIA_GROUP_MAX_SIZE: int = 10
#mediagroup maximum 10
chatid = int(-1001645629132)
# chatid = "568343456"
telegram_client = Client("my_account")


def start_bot():
    telegram_client.start()
    # Temporary files
    listMedia = []
    message = None
    while True:
        if message_queue.qsize() > 0 and message == None:
            message = message_queue.get()
            for media in message.url_medias:
                if "webm" in media:
                    file = convert_webm_to_mp4(media)
                    listMedia.append(file)
                else:
                    #listMedia.append(download_file(media))
                    listMedia.append(media)

        if len(listMedia) == 1:
            #TODO Exception handling
            try:
                sended_messages = telegram_client.send_video(chatid, video=listMedia[0], supports_streaming=True,
                                    caption="<a href=\"" + message.url_message + "\">" + message.name_thread + "</a>",
                                    parse_mode="html")
                if sended_messages:
                    # After sending, remove files
                    clean(listMedia)
                    listMedia.clear()
                    message = None
                    
            except FloodWait as e:
                asyncio.sleep(e.x)
            except MediaEmpty as e:
                print(e.x)

        elif len(listMedia) > 1:
            media_list = list(
                map(lambda input_media: InputMediaVideo(media=input_media, supports_streaming=True),
                    listMedia))
            media_list[0].caption = "<a href=\"" + message.url_message + "\">" + message.name_thread + "</a>"
            media_list[0].parse_mode = "html"

            try:
                sended_messages = telegram_client.send_media_group(chatid, media=media_list)
                if sended_messages:
                    message = None
                    # After sending, remove files
                    clean(listMedia)
                    listMedia.clear()
            except FloodWait as e:
                asyncio.sleep(e.x)
            except MediaEmpty as e:
                print(e.x)
        time.sleep(2)


def clean(listMedias):
    for media in listMedias:
        if not ('http' in media):
            os.remove(media)


if __name__ == '__main__':
    # message_queue.put(Message("Test Thread", 'https://2ch.hk/b/res/263260903.html#263261067',
    #                           ['https://2ch.hk/b/src/263260903/16449513358100.mp4']))
    # message_queue.put(Message("Test Thread 2", 'https://2ch.hk/b/res/263260903.html#263261067',
    #                           ['https://2ch.hk/b/src/263260903/16449513358100.mp4',
    #                            'https://2ch.hk/b/src/263260903/16449513358100.mp4']))
    start_bot()
