import asyncio
from pyrogram import Client
from pyrogram.handlers import MessageHandler

app = Client("my_account")

# await app.send_message("-1001645629132", "dssdf")

def dump(client, message):
    print(message)


app.add_handler(MessageHandler(dump))
app.run()
# asyncio.run(main())
