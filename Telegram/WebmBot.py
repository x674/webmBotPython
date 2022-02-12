import asyncio

from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)

app = Client("my_bot")


@app.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    # Get bot results for "hello" from the inline bot @vid
    bot_results = app.get_inline_bot_results("vid", "hello")

    # Send the first result (bot_results.results[0]) to your own chat (Saved Messages)
    app.send_inline_bot_result("me", bot_results.query_id, bot_results.results[0].id)
    await message.reply_text("Helo iam Youtube Video Search\nUse in inline mode")


@app.on_inline_query()
def answer(client, inline_query):
    print(inline_query)


def start_bot():
    asyncio.run(app.run())
