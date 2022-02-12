import asyncio
import time
from queue import Queue

import requests

message_queue = Queue()
host2ch = "https://2ch.hk"
url2chCatalog = "https://2ch.hk/b/catalog.json"

"""Return list current threads"""


async def update_threads():
    threads = await get_2ch_threads()
    for thread in threads:
        get_media_from_thread(thread["num"])
        # anti dos
        time.sleep(5)


async def get_2ch_threads():
    list_threads = requests.get(url2chCatalog).json()["threads"]
    return list_threads


def get_media_from_thread(idThread):
    url_api = host2ch + "/b/res/" + idThread + ".json"
    thread = requests.get(url_api).json()
    posts = thread["threads"][0]["posts"]
    url_list = []
    for post in posts:
        for media in post["files"]:
            if any(type in media["name"] for type in ["mp4", "webm"]):
                url_list.append(media["path"])
        url_thread_message = host2ch + "/b/res/" + idThread + ".html" + "#" + str(post["num"])
        if len(url_list) > 0:
            message_queue.put([thread['title'], url_thread_message, url_list])


asyncio.run(update_threads())
