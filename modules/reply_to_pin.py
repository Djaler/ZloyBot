from telegram.ext import CommandHandler

from filters import PermittedChatFilter, supergroup_filter


class ReplyToPin:
    _PINNED_MESSAGE = '☝️️'
    _NOT_PINNED_MESSAGE = 'Закрепленное сообщение отсутствует.'

    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id

        self.permitted_chat_filter = PermittedChatFilter([self._chat_id])

    def add_handlers(self, add_handler):
        add_handler(CommandHandler('pinned', callback=self.reply_to_pin,
                                   filters=self.permitted_chat_filter & supergroup_filter))

    def reply_to_pin(self, bot, update):
        message = update.message

        chat = bot.get_chat(message.chat_id)

        if chat.pinned_message:
            chat.pinned_message.reply_text(self._PINNED_MESSAGE, disable_notification=True)
        else:
            message.reply_text(self._NOT_PINNED_MESSAGE, disable_notification=True)
