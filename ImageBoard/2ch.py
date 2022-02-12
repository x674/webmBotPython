import asyncio
import requests

host2ch = "https://2ch.hk"
url2chCatalog = "https://2ch.hk/b/catalog.json"

"""Return list current threads"""


async def start():
    threads = await get_2ch_threads()
    for thread in threads:
        get_media_from_thread(thread["num"])


async def get_2ch_threads():
    list_threads = requests.get(url2chCatalog).json()["threads"]
    return list_threads


def get_media_from_thread(idThread):
    url = host2ch + "/b/res/" + idThread + ".json"
    thread = requests.get(url).json()
    posts = thread["threads"][0]["posts"]
    list_medias = []
    for post in posts:
        for media in post["files"]:
            if any(type in media["name"] for type in ["mp4","webm"]):
                list_medias.append(media)


    return list_medias


asyncio.run(start())
