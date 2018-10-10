import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Filters

from filters import PermittedChatFilter, supergroup_filter
from utils import get_username_or_name
from utils import set_callback_data, process_callback_query, get_callback_data


class UserJoinCaptcha:
    _ON_JOIN_MESSAGE = 'Эй, {username}!\n' \
                       'Мы отобрали твою свободу слова, пока ты не тыкнешь сюда 👇'
    _ON_APPROVE_MESSAGES = [
        'Ты смог нажать на кнопку! Уровень твоего развития уже выше, чем у большинства чертей из этого чата.',
        'Ты справился. Ты или кусок мяса, или ИИ, прямо как я']
    _ON_ACCESS_RESTRICTED_MESSAGES = ['КУДА ЖМЁШЬ?!️! РУКУ УБРАЛ!', 'У тебя здесь нет власти!']
    _INLINE_BUTTON_TEXTS = ['Аниме - моя жизнь', 'Я отдаю свою жизнь и честь Ночному Дозору']

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
        new_members = message.new_chat_members

        for member in new_members:
            if member.is_bot:
                continue

            bot.restrict_chat_member(self._chat_id,
                                     member.id,
                                     can_send_messages=False)

            keyboard = [[InlineKeyboardButton(random.choice(self._INLINE_BUTTON_TEXTS),
                                              callback_data=set_callback_data(member.id))]]
            reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

            bot.send_message(
                self._chat_id,
                text=self._ON_JOIN_MESSAGE.format(username=member.name),
                reply_markup=reply_markup
            )

    @process_callback_query
    def _process_captcha(self, bot, update):
        query = update.callback_query
        user = query.from_user

        suspect_id = int(get_callback_data(query.data))

        username = get_username_or_name(user)

        if user.id != suspect_id:
            bot.answer_callback_query(query.id, random.choice(self._ON_ACCESS_RESTRICTED_MESSAGES),
                                      show_alert=True)
            return

        bot.restrict_chat_member(self._chat_id,
                                 suspect_id,
                                 can_send_messages=True,
                                 can_send_media_messages=True,
                                 can_send_other_messages=True,
                                 can_add_web_page_previews=True)

        query.message.delete()
