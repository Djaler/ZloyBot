import random

from telegram.ext import CommandHandler, Filters, MessageHandler

from model import LastUsers, User
from utils import get_username_or_name


class KtoZloy:
    _LAST_USERS_MAX_SIZE = 10

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
            'username': get_username_or_name(message.from_user)})

        LastUsers.delete().where(LastUsers.user == user).execute()

        LastUsers.create(user=user)

        last_ids = [row.id for row in LastUsers.select(LastUsers.id).order_by(LastUsers.id.desc())]

        if len(last_ids) > self._LAST_USERS_MAX_SIZE:
            border_id = last_ids[self._LAST_USERS_MAX_SIZE - 1]
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

        last_usernames = [row.username for row in User.select(User.username).where(User.username != "")]

        random_user = random.choice(last_usernames)

        if random_user == get_username_or_name(message.from_user):
            random_user = 'ты'
        bot.sendMessage(chat_id=chat_id, text='%s злой' % random_user)
