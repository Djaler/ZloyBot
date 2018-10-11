from peewee import DoesNotExist
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler

from filters import PermittedChatFilter
from model import BlockedStickerpack
from utils import is_user_group_admin, get_username_or_name, grouper
from utils import set_callback_data, process_callback_query, get_callback_data


class BlockStickerpack:
    _STICKER_ADD_URL = 'https://t.me/addstickers/'
    _ADMIN_RESTRICTION_MESSAGE = 'Эта функция предназначена только для админов!'
    _NO_STICKERPACKS_BLOCKED_MESSAGE = 'Заблокированных стикерпаков *нет*.'

    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id

        self.permitted_chat_filter = PermittedChatFilter([self._admin_id, self._chat_id])

    def add_handlers(self, add_handler):
        add_handler(MessageHandler(
            self.permitted_chat_filter & ~Filters.private & Filters.sticker,
            self._watchdog))
        add_handler(CommandHandler('block_stickerpack', callback=self._block, filters=self.permitted_chat_filter))
        add_handler(CommandHandler('unblock_stickerpack', callback=self._unblock, filters=self.permitted_chat_filter))
        add_handler(CallbackQueryHandler(self._unblock_stickerpack_button))

    def _get_stickers_link(self, stickerpack_name):
        return self._STICKER_ADD_URL + stickerpack_name

    @staticmethod
    def _get_blocked_stickerpacks():
        return BlockedStickerpack.select()

    def _block(self, bot, update):
        message = update.message

        if message.from_user.id != self._admin_id and not is_user_group_admin(bot, message.from_user.id,
                                                                              message.chat_id, self._admin_id):
            message.reply_text(text=self._ADMIN_RESTRICTION_MESSAGE, quote=False)
            return

        if message.reply_to_message is None or message.reply_to_message.sticker is None:
            message.reply_text(text='Команда предназначена только для ответа на сообщения со стикером!', quote=False)
            return

        sticker = message.reply_to_message.sticker

        stickerpack, created = BlockedStickerpack.get_or_create(name=sticker.set_name)

        pack_name = stickerpack.name
        pack_link = self._get_stickers_link(pack_name)

        if not created:
            response_text = f'Стикерпак [{pack_name}]({pack_link}) *уже заблокирован*.'
        else:
            # mention_markdown позволяет кликнуть по пользователю и глянуть кто это, вместо простого имени / юзернейма
            sticker_from = message.reply_to_message.from_user.mention_markdown()
            who_block = message.from_user.mention_markdown()

            response_text = f'Стикерпак [{pack_name}]({pack_link}) успешно *заблокирован*!\n' \
                            f'Стикер отправил: {sticker_from} | Заблокировал: {who_block}'

        message.reply_text(text=response_text, parse_mode=ParseMode.MARKDOWN, quote=False)

    def _unblock(self, bot, update):
        message = update.message

        if message.from_user.id != self._admin_id and not is_user_group_admin(bot, message.from_user.id,
                                                                              message.chat_id, self._admin_id):
            message.reply_text(text=self._ADMIN_RESTRICTION_MESSAGE, quote=False)
            return

        blocked_stickerpacks = self._get_blocked_stickerpacks()

        packs_list = []
        buttons = []

        if blocked_stickerpacks:
            for index, stickerpack in enumerate(blocked_stickerpacks, start=1):
                packs_list.append(f'{index}. [{stickerpack.name}]({self._get_stickers_link(stickerpack.name)})')
                buttons.append(
                    InlineKeyboardButton(
                        text=str(index),
                        callback_data=set_callback_data(stickerpack.id))
                )

            response_text = '*Заблокированные стикерпаки:*\n{}\n\nКакой *разблокировать*?'.format("\n".join(packs_list))

            keyboard = grouper(buttons, 5)  # в одном ряду будет 5 кнопок, так как текст на каждой из них короткий
            reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
        else:
            response_text = self._NO_STICKERPACKS_BLOCKED_MESSAGE
            reply_markup = None

        message.reply_text(text=response_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup, quote=False)

    @process_callback_query
    def _unblock_stickerpack_button(self, bot, update):
        query = update.callback_query

        if query.from_user.id != self._admin_id and not is_user_group_admin(bot, query.from_user.id,
                                                                            query.message.chat_id, self._admin_id):
            bot.answer_callback_query(query.id, self._ADMIN_RESTRICTION_MESSAGE, show_alert=True)
            return

        message = query.message

        pack_id = get_callback_data(query.data)

        try:
            stickerpack = BlockedStickerpack.get(BlockedStickerpack.id == pack_id)
        except DoesNotExist:
            response_text = f'Выбранный стикерпак *не был найден* в списке заблокированных.'
        else:
            pack_name = stickerpack.name
            pack_link = self._get_stickers_link(pack_name)

            stickerpack.delete_instance()

            response_text = f'Стикерпак [{pack_name}]({pack_link}) успешно *разблокирован*.'

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
