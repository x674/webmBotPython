import asyncio
from pyrogram import Client


async def main():
    async with Client("my_account") as app:
        await app.send_message("-1001645629132", "Greetings from **Pyrogram**!")

asyncio.run(main())