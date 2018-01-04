from telegram.ext import BaseFilter

from settings import CHAT_ID, ADMIN_ID


class ReplyToBotFilter(BaseFilter):
    def filter(self, message):
        bot_username = message.bot.username
        reply = message.reply_to_message

        return bool(reply) and reply.from_user.name == bot_username


reply_to_bot_filter = ReplyToBotFilter()


class PermittedChatFilter(BaseFilter):
    def filter(self, message):
        return message.chat_id in (ADMIN_ID, CHAT_ID)


permitted_chat_filter = PermittedChatFilter()
