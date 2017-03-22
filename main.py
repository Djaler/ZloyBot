import os

from bot import Bot

token = os.environ.get("TOKEN")
admin_id = os.environ.get("ADMIN_ID")
chat_id = os.environ.get("CHAT_ID")

bot = Bot(token, chat_id, admin_id)
bot.run()
