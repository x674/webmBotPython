import asyncio
import time

from pyrogram.types import InputMediaVideo
from pyrogram import Client
from ImageBoard.dvach import message_queue, Message

chatid = int(-1001645629132)
# chatid = "568343456"
telegram_client = Client("my_account")
InputMediaVideo("video.mp4", caption="video caption")


def start_bot():
    telegram_client.start()
    while True:
        if message_queue.qsize() > 0:
            message = message_queue.get()
            if len(message.url_medias) == 1:
                telegram_client.send_video(chatid, video=message.url_medias[0], supports_streaming=True,
                                           caption="<a href=\"" + message.url_message + "\">" + message.name_thread + "</a>",
                                           parse_mode="html")
            elif len(message.url_medias) > 1:
                media_list = list(
                    map(lambda input_media: InputMediaVideo(media=input_media, supports_streaming=True),
                        message.url_medias))
                media_list[0].caption = "<a href=\"" + message.url_message + "\">" + message.name_thread + "</a>"
                media_list[0].parse_mode = "html"
                telegram_client.send_media_group(chatid, media=media_list)
        time.sleep(2)


if __name__ == '__main__':
    # message_queue.put(Message("Test Thread", 'https://2ch.hk/b/res/263260903.html#263261067',
    #                           ['https://2ch.hk/b/src/263260903/16449513358100.mp4']))
    # message_queue.put(Message("Test Thread 2", 'https://2ch.hk/b/res/263260903.html#263261067',
    #                           ['https://2ch.hk/b/src/263260903/16449513358100.mp4',
    #                            'https://2ch.hk/b/src/263260903/16449513358100.mp4']))
    start_bot()
