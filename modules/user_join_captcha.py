from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Filters

from filters import PermittedChatFilter, supergroup_filter
from utils import get_username_or_name


class UserJoinCaptcha:
    _ON_JOIN_MESSAGE = 'Привет, {username}!\n' \
                       'Сейчас ты ничего не можешь писать в чат.\n' \
                       'Чтобы снять это ограничение - нажми на кнопку под этим сообщением! 👇'
    _ON_APPROVE_MESSAGE = '{username}, ты доказал, что ты не бот. 🤓\n' \
                          'Либо очень умный бот. 🤖 Нам такие тоже подходят.\n\n' \
                          'Добро пожаловать. 👊'
    _ON_ACCESS_RESTRICTED_MESSAGE = 'ЭТО НЕ ТВОЯ БИТВА, {username}! ⚔️'
    _INLINE_BUTTON_TEXT = 'Я не бот! ✊️'

    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id

        self.permitted_chat_filter = PermittedChatFilter([self._chat_id])

    def add_handlers(self, add_handler):
        add_handler(MessageHandler(
            filters=self.permitted_chat_filter & supergroup_filter & Filters.status_update.new_chat_members,
            callback=self._send_captcha))

        add_handler(CallbackQueryHandler(self._process_captcha))

    def _send_captcha(self, bot, update):
        message = update.message
        user = update.message.from_user

        if user.id == self._admin_id:
            return

        username = get_username_or_name(user)

        bot.restrict_chat_member(self._chat_id,
                                 user.id,
                                 can_send_messages=False)

        keyboard = [[InlineKeyboardButton(self._INLINE_BUTTON_TEXT, callback_data=f'{__name__}/{user.id}')]]
        reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

        message.reply_text(
            text=self._ON_JOIN_MESSAGE.format(username=username),
            reply_markup=reply_markup)

    def _process_captcha(self, bot, update):
        query = update.callback_query
        user = query.from_user

        module, suspect_id = query.data.split('/')

        if module != __name__:
            return

        suspect_id = int(suspect_id)

        username = get_username_or_name(user)

        if user.id != suspect_id:
            bot.answer_callback_query(query.id, self._ON_ACCESS_RESTRICTED_MESSAGE.format(username=username),
                                      show_alert=True)
            return

        bot.restrict_chat_member(self._chat_id,
                                 suspect_id,
                                 can_send_messages=True,
                                 can_send_media_messages=True,
                                 can_send_other_messages=True)

        query.message.edit_text(text=self._ON_APPROVE_MESSAGE.format(username=username))
