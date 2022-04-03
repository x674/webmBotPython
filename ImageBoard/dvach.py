import asyncio
import time
from queue import Queue

import requests

message_queue = Queue()
host2ch = "https://2ch.hk"
url2chCatalog = "https://2ch.hk/b/catalog.json"


class Message:
    def __init__(self, name_thread, url_message, url_medias):
        self.name_thread = name_thread
        self.url_message = url_message
        self.url_medias = url_medias


"""Return list current threads"""


def update_threads():
    threads = list(filter(lambda thread: any(type in thread['subject'].lower() for type in ["фап"]),
                          get_2ch_threads()))
    for thread in threads:
        get_media_from_thread(thread["num"])
        print("total message: " + str(message_queue.qsize()))
        # anti dos
        time.sleep(5)



def get_2ch_threads():
    list_threads = requests.get(url2chCatalog).json()["threads"]
    return list_threads


def get_media_from_thread(idThread):
    url_api = host2ch + "/b/res/" + idThread + ".json"
    thread = requests.get(url_api).json()
    posts = thread["threads"][0]["posts"]
    for post in posts:
        url_list = []
        for media in post["files"]:
            #            if any(type in media["name"] for type in ["mp4", "webm"]):
            if any(type in media["name"] for type in ["mp4", "webm"]):
                url_list.append(host2ch + media["path"])
        url_thread_message = ""
        if len(url_list) > 0:
            url_thread_message = host2ch + "/b/res/" + idThread + ".html" + "#" + str(post["num"])
            message_queue.put(Message(thread['title'], url_thread_message, url_list))


if __name__ == '__main__':
    update_threads()
