import logging
import os
import traceback

from telegram import ParseMode, TelegramError
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler, \
    Updater

from model import init_database
from modules.admin import Admin
from modules.forward import Forward
from modules.kto_zloy import KtoZloy
from modules.primitive_response import PrimitiveResponse
from modules.random_reaction import random_reaction
from modules.resolve import resolve
from modules.statistic import Statistic


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
    def __init__(self, token, chat_id, admin_id):
        Dispatcher.process_update = process_update
        
        self._token = token
        self._updater = Updater(token)
        self._chat_id = int(chat_id)
        self._admin_id = int(admin_id)
        
        init_database()
        self._init_handlers()
        
        log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        logging.basicConfig(format=log_format, level=logging.WARNING)
    
    def run(self):
        port = int(os.environ.get('PORT', '5000'))
        self._updater.start_webhook(listen='0.0.0.0', port=port,
                                    url_path=self._token)
        self._updater.bot.set_webhook(os.environ.get("URL") +
                                      self._token)
        self._updater.idle()
    
    def _init_handlers(self):
        self._updater.dispatcher.add_handler(
            MessageHandler(Filters.all, random_reaction))

        statistic = Statistic(self._chat_id, self._admin_id)
        statistic.add_handlers(self._updater.dispatcher.add_handler)

        forward = Forward(self._chat_id, self._admin_id)
        forward.add_handlers(self._updater.dispatcher.add_handler)

        kto_zloy = KtoZloy(self._chat_id, self._admin_id)
        kto_zloy.add_handlers(self._updater.dispatcher.add_handler)

        self._updater.dispatcher.add_handler(
            CommandHandler('resolve', resolve, pass_args=True))
        self._updater.dispatcher.add_handler(
            CommandHandler('r', resolve, pass_args=True))

        admin = Admin(self._chat_id, self._admin_id)
        admin.add_handlers(self._updater.dispatcher.add_handler)

        primitive_response = PrimitiveResponse(self._chat_id)
        primitive_response.add_handlers(self._updater.dispatcher.add_handler)
        
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
        bot.send_message(chat_id=self._admin_id, text='```' + text + '```',
                         parse_mode=ParseMode.MARKDOWN)
