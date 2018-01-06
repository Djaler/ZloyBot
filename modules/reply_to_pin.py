from telegram.ext import CommandHandler

from filters import PermittedChatFilter, supergroup_filter


class ReplyToPin:
    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id

        self.permitted_chat_filter = PermittedChatFilter([self._chat_id])

        self.last_message_id = None

    def add_handlers(self, add_handler):
        add_handler(CommandHandler('pinned', callback=self.reply_to_pin,
                                   filters=self.permitted_chat_filter & supergroup_filter))

    def reply_to_pin(self, bot, update):
        message = update.message

        chat = bot.get_chat(message.chat_id)
        if chat.pinned_message is None:
            return

        chat.pinned_message.reply_text('☝️️', disable_notification=True)

        self.last_message_id = message.message_id
