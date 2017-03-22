from random import randint

from peewee import fn
from telegram.ext import CommandHandler

from model import User


class KtoZloy:
    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id
    
    def add_handlers(self, add_handler):
        add_handler(CommandHandler('ktozloy', self._kto_zloy))
    
    @staticmethod
    def _kto_zloy(bot, update):
        message = update.message
        
        chat_id = message.chat_id
        if randint(1, 10) == 1:
            bot.sendMessage(chat_id=chat_id, text='я злой ¯\_(ツ)_/¯')
            return
        
        random_user = User \
            .select() \
            .order_by(fn.Random()) \
            .limit(1) \
            .get().username
        if random_user == message.from_user.username:
            random_user = 'ты'
        bot.sendMessage(chat_id=chat_id, text='%s злой' % random_user)
