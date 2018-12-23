import logging
import traceback

from telegram import ParseMode, TelegramError
from telegram.ext import CommandHandler, Dispatcher, Updater

from model import init_database
from modules.admin import Admin
from modules.block_stickerpack import BlockStickerpack
from modules.forward import Forward
from modules.kto_zloy import KtoZloy
from modules.pay_respect import pay_respect
from modules.reactions import Reactions
from modules.reply_to_pin import ReplyToPin
from modules.resolve import resolve
from modules.statistic import Statistic
from modules.user_join_captcha import UserJoinCaptcha
from settings import ADMIN_ID, CHAT_ID, ENV, PORT, TOKEN, URL
from settings import USER_JOIN_CAPTCHA_ENABLED


def process_update(obj, update):
    if isinstance(update, TelegramError):
        obj.dispatch_error(None, update)
    
    else:
        for group in obj.groups:
            for handler in obj.handlers[group]:
                try:
                    if handler.check_update(update):
                        handler.handle_update(update, obj)
                except Exception as e:
                    try:
                        obj.dispatch_error(update, e)
                    except Exception:
                        obj.logger.exception(
                            'An uncaught error was raised while '
                            'handling the error')


class Bot:
    def __init__(self):
        Dispatcher.process_update = process_update

        self._updater = Updater(TOKEN)
        
        init_database()
        self._init_handlers()
        
        log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        logging.basicConfig(format=log_format, level=logging.WARNING)
    
    def run(self):
        if ENV == "prod":
            self._updater.start_webhook(listen='0.0.0.0', port=PORT,
                                        url_path=TOKEN)
            self._updater.bot.set_webhook(URL + TOKEN)
            self._updater.idle()
        else:
            self._updater.start_polling(poll_interval=1)
    
    def _init_handlers(self):
        statistic = Statistic(CHAT_ID, ADMIN_ID)
        statistic.add_handlers(self._updater.dispatcher.add_handler)

        forward = Forward(CHAT_ID, ADMIN_ID)
        forward.add_handlers(self._updater.dispatcher.add_handler)

        kto_zloy = KtoZloy(CHAT_ID, ADMIN_ID)
        kto_zloy.add_handlers(self._updater.dispatcher.add_handler)

        self._updater.dispatcher.add_handler(
            CommandHandler('resolve', resolve, pass_args=True))
        self._updater.dispatcher.add_handler(
            CommandHandler('r', resolve, pass_args=True))

        self._updater.dispatcher.add_handler(
            CommandHandler('f', pay_respect))

        admin = Admin(CHAT_ID, ADMIN_ID)
        admin.add_handlers(self._updater.dispatcher.add_handler)

        reactions = Reactions(CHAT_ID)
        reactions.add_handlers(self._updater.dispatcher.add_handler)

        block_stickerpack = BlockStickerpack(CHAT_ID, ADMIN_ID)
        block_stickerpack.add_handlers(self._updater.dispatcher.add_handler)

        reply_to_pin = ReplyToPin(CHAT_ID, ADMIN_ID)
        reply_to_pin.add_handlers(self._updater.dispatcher.add_handler)

        if USER_JOIN_CAPTCHA_ENABLED:
            user_join_captcha = UserJoinCaptcha(CHAT_ID, ADMIN_ID)
            user_join_captcha.add_handlers(self._updater.dispatcher.add_handler)
        
        self._updater.dispatcher.add_error_handler(self._error)
    
    def _error(self, bot, update, error):
        def parse_dict(dictionary, level):
            text = []
            for key in dictionary.keys():
                value = dictionary[key]
                if not value:
                    continue
                if isinstance(value, dict):
                    value = parse_dict(value, level + 1)
                text.append('\t' * level + '{0}: {1}'.format(key, value))
            return '\n' + '\n'.join(text)
        
        if not update:
            return
        
        text = parse_dict(update.to_dict(),
                          1) + '\n\n' + traceback.format_exc()
        logging.warning(text)
        bot.send_message(chat_id=ADMIN_ID, text='```' + text + '```',
                         parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
