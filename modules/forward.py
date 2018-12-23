from telegram.ext import Filters, MessageHandler, CommandHandler

from utils import get_username_or_name


class Forward:
    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id
    
    def add_handlers(self, add_handler):
        add_handler(MessageHandler(Filters.all, self._forward))
        add_handler(CommandHandler('me', self._me, pass_args=True))
    
    def _forward(self, bot, update):
        message = update.message
        if message.chat_id not in (self._chat_id, self._admin_id):
            bot.forwardMessage(message_id=message.message_id,
                               from_chat_id=message.chat_id,
                               chat_id=self._admin_id)
            text = ['chat_id = {}'.format(message.chat_id)]
            if message.chat.title:
                text.append('title = {}'.format(message.chat.title))
            bot.sendMessage(chat_id=self._admin_id, text='\n'.join(text))

    def _me(self, bot, update, args):
        message = update.message

        text = "{0} {1}".format(get_username_or_name(message.from_user), ' '.join(args))
        bot.sendMessage(chat_id=self._chat_id, text=text)
