import asyncio
import os
import time
from typing import List

from VideoUtils.webmConverter import convert_webm_to_mp4, download_file
from VideoUtils.Utils import has_audio_streams, generate_thumbnail

from pyrogram.types import InputMediaVideo, InputMediaAnimation
from pyrogram import Client
from pyrogram.errors import FloodWait, MediaEmpty
from ImageBoard.dvach import message_queue, Message

MEDIA_GROUP_MAX_SIZE: int = 10
# mediagroup maximum 10
chatid = int(-1001645629132)
# chatid = "568343456"
telegram_client = Client("my_account")


class MediaFile:
    def __init__(self, pathMedia, pathThumbnail):
        self.pathMedia = pathMedia
        self.pathThumbnail = pathThumbnail


listMedia: List[MediaFile] = []


def start_bot():
    telegram_client.start()
    # Temporary files
    message = None
    while True:
        if message_queue.qsize() > 0 and message == None:
            message = message_queue.get()
            for url_media in message.url_medias:
                if "mp4" in url_media:
                    mediafile = download_file(url_media)
                    thumbnail = generate_thumbnail(mediafile)
                    listMedia.append(MediaFile(mediafile, thumbnail))
                    # listMedia.append(media)
                elif "webm" in url_media:
                    mediafile = convert_webm_to_mp4(url_media)
                    thumbnail = generate_thumbnail(mediafile)
                    listMedia.append(MediaFile(mediafile, thumbnail))
                # anti dos
                time.sleep(4)
        elif message:
            caption = "<a href=\"" + message.url_message + "\">" + message.name_thread
            if len(listMedia) == 1:
                # TODO Exception handling
                try:
                    sent_messages = telegram_client.send_video(
                        chatid, video=listMedia[0].pathMedia,
                        thumb=listMedia[0].pathThumbnail,
                        supports_streaming=True,
                        caption="<a href=\"" + message.url_message + "\">" + message.name_thread + "</a>",
                        parse_mode="html"
                    )
                    if sent_messages:
                        # After sending, remove files
                        clean(listMedia)
                        listMedia.clear()
                        message = None

                except FloodWait as e:
                    asyncio.sleep(e.x)

            elif len(listMedia) > 1:

                # create list media to sent in group
                media_list = []
                for media in listMedia:
                    # if media file contains audio then it can be sent in a group
                    if has_audio_streams(media.pathMedia):
                        media_list.append(
                            InputMediaVideo(media=media.pathMedia, thumb=media.pathThumbnail, supports_streaming=True))
                    # else, we send it immediately as an animation
                    else:
                        try:
                            telegram_client.send_animation(chatid,
                                                           animation=media.pathMedia,
                                                           thumb=media.pathThumbnail,
                                                           caption=caption,
                                                           parse_mode="html")
                            time.sleep(4)
                        except FloodWait as e:
                            asyncio.sleep(e.x)
                media_list[0].caption = caption
                media_list[0].parse_mode = "html"
                try:
                    sent_messages = telegram_client.send_media_group(chatid, media=media_list)
                    if sent_messages:
                        message = None
                        # After sending, remove files
                        clean(listMedia)
                        listMedia.clear()
                except FloodWait as e:
                    asyncio.sleep(e.x)
            time.sleep(4)


def clean(listMedias):
    for media in listMedias:
        if not ('http' in media.pathMedia):
            os.remove(media.pathMedia)
            os.remove(media.pathThumbnail)


if __name__ == '__main__':
    # message_queue.put(Message("Test Thread", 'https://2ch.hk/b/res/263260903.html#263261067',
    #                           ['https://2ch.hk/b/src/263260903/16449513358100.mp4']))
    # message_queue.put(Message("Test Thread 2", 'https://2ch.hk/b/res/263260903.html#263261067',
    #                           ['https://2ch.hk/b/src/263260903/16449513358100.mp4',
    #                            'https://2ch.hk/b/src/263260903/16449513358100.mp4']))
    start_bot()
