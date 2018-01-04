from telegram.ext import CommandHandler, Filters, MessageHandler

from model import User, UserMessagesInfo


class Statistic:
    def __init__(self, chat_id, admin_id):
        self._chat_id = chat_id
        self._admin_id = admin_id
    
    def add_handlers(self, add_handler):
        add_handler(MessageHandler(Filters.text, self._update_statistic))
        add_handler(CommandHandler('top10', self._top10))
        add_handler(CommandHandler('statistic', self._display_statistic))

    def _top10(self, bot, update):
        message = update.message
        
        if message.chat_id not in (self._chat_id, self._admin_id):
            return
        
        top10 = UserMessagesInfo \
            .select() \
            .order_by(UserMessagesInfo.number.desc()) \
            .limit(10)
        
        if not top10:
            return
        
        text = '\n'.join(
            '{0}. {1} - {2}'.format(index + 1, info.user.username, info.number)
            for index, info in enumerate(top10))
        bot.sendMessage(chat_id=message.chat_id, text=text,
                        reply_to_message_id=message.message_id)
    
    def _display_statistic(self, bot, update):
        message = update.message
        
        if message.chat_id not in (self._chat_id, self._admin_id):
            return

        user, _ = User.get_or_create(user_id=message.from_user.id,
                                     defaults={
                                         'username':
                                             message.from_user.name})
        
        if not user.user_messages_info.exists():
            bot.sendMessage(chat_id=message.chat_id,
                            reply_to_message_id=message.message_id,
                            text='Ты не писал ещё ничего, алло')
            return
        
        number = user.user_messages_info.get().number
        
        if 11 <= number % 100 <= 14:
            words = 'нужных сообщений'
        elif number % 10 == 1:
            words = 'нужное сообщение'
        elif 2 <= number % 10 <= 4:
            words = 'нужных сообщения'
        else:
            words = 'нужных сообщений'
        
        bot.sendMessage(chat_id=message.chat_id,
                        reply_to_message_id=message.message_id,
                        text='ты написал {0} никому не {1}.'.format(number,
                                                                    words))
    
    def _update_statistic(self, bot, update):
        message = update.message
        if message.chat_id != self._chat_id:
            return
        
        user, _ = User.get_or_create(user_id=message.from_user.id, defaults={
            'username': message.from_user.name})
        
        if user.username != message.from_user.name:
            user.username = message.from_user.name
            user.save()
        
        user_messages_info, _ = UserMessagesInfo \
            .get_or_create(user=user, defaults={'number': 0})
        user_messages_info.number += 1
        user_messages_info.save()
