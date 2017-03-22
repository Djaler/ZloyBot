from telegram.ext import CommandHandler

from model import database


class Admin:
    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id
    
    def add_handlers(self, add_handler):
        add_handler(CommandHandler('send', self._send_to_chat, pass_args=True))
        add_handler(CommandHandler('send_to', self._send_to, pass_args=True))
        add_handler(CommandHandler('sql', self._sql, pass_args=True))
    
    def _send_to_chat(self, bot, update, args):
        message = update.message
        if message.from_user.id == self._admin_id:
            text = ' '.join(args)
            bot.sendMessage(chat_id=self._chat_id, text=text)
        else:
            bot.sendMessage(chat_id=message.chat_id, text='NIET',
                            reply_to_message_id=message.message_id)
    
    def _send_to(self, bot, update, args):
        message = update.message
        if message.from_user.id == self._admin_id:
            to_id = int(args[0])
            text = ' '.join(args[1:])
            bot.sendMessage(chat_id=to_id, text=text)
        else:
            bot.sendMessage(chat_id=message.chat_id, text='NIET',
                            reply_to_message_id=message.message_id)
    
    def _sql(self, bot, update, args):
        message = update.message
        if message.from_user.id == self._admin_id:
            text = ' '.join(args)
            result = database.execute_sql(text).fetchall()
            if text.startswith('select'):
                if result:
                    text = '\n'.join('{0}. {1}'.format(index + 1, ' - '.join(
                        str(el) for el in row)) for index, row in
                                     enumerate(result))
                else:
                    text = 'Нет результатов'
                bot.sendMessage(chat_id=message.chat_id, text=text,
                                reply_to_message_id=message.message_id)
        else:
            bot.sendMessage(chat_id=message.chat_id, text='NIET',
                            reply_to_message_id=message.message_id)
