from peewee import DoesNotExist
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler

from model import BlockedStickerpack
from utils import is_user_group_admin
from filters import PermittedChatFilter


class BlockStickerpack:
    _STICKER_ADD_URL = 'https://t.me/addstickers/'
    _ADMIN_RESTRICTION_MESSAGE = 'Эта функция предназначена только для администраторов бота!'
    _NO_STICKERPACKS_BLOCKED_MESSAGE = 'Заблокированных стикерпаков пока нет.'

    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id

        self.permitted_chat_filter = PermittedChatFilter([self._admin_id, self._chat_id])

    def add_handlers(self, add_handler):
        add_handler(MessageHandler(PermittedChatFilter([self._admin_id, self._chat_id]) & ~Filters.private & Filters.sticker, self._watchdog))
        add_handler(CommandHandler('block_stickerpack',
                                   callback=self._block,
                                   filters=self.permitted_chat_filter))
        add_handler(CommandHandler('unblock_stickerpack',
                                   callback=self._unblock,
                                   filters=self.permitted_chat_filter))
        add_handler(CommandHandler('list_stickerpacks',
                                   callback=self._list,
                                   filters=self.permitted_chat_filter))
        add_handler(CallbackQueryHandler(self._unblock_stickerpack_button))

    def _get_stickers_link(self, stickerpack_name):
        return self._STICKER_ADD_URL + stickerpack_name

    @staticmethod
    def _get_blocked_stickerpacks():
        return BlockedStickerpack.select()

    def _list(self, bot, update):
        message = update.message

        queryset = self._get_blocked_stickerpacks()

        if queryset:
            stickerpacks_list = (f'{index}. [{stickerpack.name}]({self._get_stickers_link(stickerpack.name)})'
                                 for index, stickerpack in enumerate(queryset, start=1))
            response_text = 'Заблокированные стикерпаки:\n' + '\n'.join(stickerpacks_list)
        else:
            response_text = self._NO_STICKERPACKS_BLOCKED_MESSAGE

        message.reply_text(text=response_text, parse_mode=ParseMode.MARKDOWN, quote=False)

    def _block(self, bot, update):
        message = update.message

        if message.from_user.id != self._admin_id and not is_user_group_admin(bot, message.from_user.id, message.chat_id):
            message.reply_text(text=self._ADMIN_RESTRICTION_MESSAGE, quote=False)
            return

        if message.reply_to_message is None or message.reply_to_message.sticker is None:
            message.reply_text(text='Команда предназначена только для ответа на сообщения со стикером!', quote=False)
            return

        sticker = message.reply_to_message.sticker

        stickerpack, created = BlockedStickerpack.get_or_create(name=sticker.set_name)

        if not created:
            response_text = f'Стикерпак [{stickerpack.name}]({self._get_stickers_link(stickerpack.name)}) уже заблокирован.'
        else:
            response_text = f'Стикерпак [{stickerpack.name}]({self._get_stickers_link(stickerpack.name)}) успешно заблокирован!\n' \
                            f'Стикер отправил: {message.reply_to_message.from_user.name} | Заблокировал: {message.from_user.name}'

        message.reply_text(text=response_text, parse_mode=ParseMode.MARKDOWN, quote=False)

    def _unblock(self, bot, update):
        message = update.message

        if message.from_user.id != self._admin_id and not is_user_group_admin(bot, message.from_user.id, message.chat_id):
            message.reply_text(text=self._ADMIN_RESTRICTION_MESSAGE, quote=False)
            return

        blocked_stickerpacks = self._get_blocked_stickerpacks()
        if not blocked_stickerpacks:
            response_text = self._NO_STICKERPACKS_BLOCKED_MESSAGE
            reply_markup = None
        else:
            response_text = 'Выберите стикерпак, который нужно разблокировать:'
            keyboard = [[InlineKeyboardButton(f'{index}. {sp.name}', callback_data=sp.name)] for index, sp in
                        enumerate(blocked_stickerpacks, start=1)]
            reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

        message.reply_text(text=response_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup, quote=False)

    def _unblock_stickerpack_button(self, bot, update):
        query = update.callback_query

        if query.from_user.id != self._admin_id and not is_user_group_admin(bot, query.from_user.id, query.message.chat_id):
            bot.answer_callback_query(query.id, self._ADMIN_RESTRICTION_MESSAGE, show_alert=True)
            return

        message = query.message

        stickerpack_name = query.data

        try:
            stickerpack = BlockedStickerpack.get(BlockedStickerpack.name == stickerpack_name)
        except DoesNotExist:
            response_text = f'Стикерпак "{stickerpack_name}" не был найден в списке заблокированных.'
        else:
            stickerpack.delete_instance()
            response_text = f'Стикерпак [{query.data}]({self._get_stickers_link(stickerpack.name)}) успешно разблокирован.'

        message.edit_text(text=response_text, parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    def _watchdog(bot, update):
        message = update.message
        sticker = message.sticker

        try:
            BlockedStickerpack.get(BlockedStickerpack.name == sticker.set_name)
        except DoesNotExist:
            return

        message.delete()
