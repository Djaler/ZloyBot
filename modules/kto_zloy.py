import random

from peewee import SQL, fn
from telegram.ext import CommandHandler, Filters, MessageHandler

from model import LastUsers, User


class KtoZloy:
    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id
    
    def add_handlers(self, add_handler):
        add_handler(CommandHandler('ktozloy', self._kto_zloy))
        add_handler(MessageHandler(Filters.all, self._update_last_users))

    def _update_last_users(self, bot, update):
        message = update.message
        if message.chat_id != self._chat_id:
            return

        user, _ = User.get_or_create(user_id=message.from_user.id, defaults={
            'username': message.from_user.name})

        LastUsers.create(user=user)

        border_id = self._get_last_users()[-1].last_id
        
        LastUsers.delete().where(
            LastUsers.id < border_id).execute()
    
    def _kto_zloy(self, bot, update):
        message = update.message
        
        chat_id = message.chat_id

        if chat_id != self._chat_id:
            return

        if random.randint(1, 10) == 1:
            bot.sendMessage(chat_id=chat_id, text='я злой ¯\_(ツ)_/¯')
            return

        last_usernames = [row.username for row in self._get_last_users()]
        
        random_user = random.choice(last_usernames)
        
        if random_user == message.from_user.name:
            random_user = 'ты'
        bot.sendMessage(chat_id=chat_id, text='%s злой' % random_user)

    @staticmethod
    def _get_last_users():
        return list(
            User.select(User.username, fn.MAX(LastUsers.id).alias("last_id"))
                .join(LastUsers)
                .where(User.username != "")
                .group_by(User.id, User.username)
                .order_by(SQL("last_id").desc())
                .limit(10))
