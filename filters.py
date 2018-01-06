from telegram import Chat
from telegram.ext import BaseFilter


class ReplyToBotFilter(BaseFilter):
    def filter(self, message):
        bot_username = message.bot.username
        reply = message.reply_to_message

        return bool(reply) and reply.from_user.username == bot_username


reply_to_bot_filter = ReplyToBotFilter()


class SuperGroupFilter(BaseFilter):
    def filter(self, message):
        return message.chat.type == Chat.SUPERGROUP


supergroup_filter = SuperGroupFilter()


class PermittedChatFilter(BaseFilter):
    def __init__(self, chat_ids):
        self._chat_ids = chat_ids

    def filter(self, message):
        return message.chat_id in self._chat_ids
