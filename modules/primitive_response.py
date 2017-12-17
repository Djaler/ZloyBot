import re
from random import choice, randint

from telegram.ext import BaseFilter, CommandHandler, Filters, MessageHandler


class ReplyToBotFilter(BaseFilter):
    def filter(self, message):
        bot_username = message.bot.username
        reply = message.reply_to_message
        
        return bool(reply) and reply.from_user.username == bot_username


reply_to_bot_filter = ReplyToBotFilter()


class PrimitiveResponse:
    def __init__(self, chat_id):
        self._chat_id = chat_id
    
    def add_handlers(self, add_handler):
        add_handler(MessageHandler(Filters.text, self.text_responses))
        add_handler(
            MessageHandler(Filters.text & reply_to_bot_filter,
                           self.reply_responses))
        add_handler(CommandHandler('me', self._me, pass_args=True))

    def text_responses(self, bot, update):
        def text_response(patterns, answer, chance=100):
            if any(re.search(pattern, text) for pattern in patterns):
                if answer.endswith('.txt'):
                    answer = self._choice_variant_from_file(answer)

                if randint(1, 100) <= chance:
                    bot.sendMessage(chat_id=chat_id, text=answer,
                                    reply_to_message_id=message_id,
                                    markdown_support=True)
        
        message = update.message
        chat_id = message.chat_id
        text = message.text.lower()
        message_id = message.message_id
        
        text_response(['ты злой', 'злой ты', 'ты - злой', 'вы злые', 'злые вы',
                       'вы - злые', 'вы все злые'], 'ты злой!')
        
        text_response(['спать', 'посплю'], 'snov.txt')
        
        text_response(['бот злой'], 'Ты не лучше.')

        text_response([r'иди на ?хуй', r'на ?хуй пошел', r'на ?хуй иди',
                       r'пошел на ?хуй'], 'nahui.txt')
        
        text_response(['бот пидор', 'бот идиот', 'бот мудак'], 'И?')
        
        text_response(['бот умер'], 'Герої не вмирають! 🇺🇦')
        
        text_response(['бот няша'], 'Спасибо, ты тоже <3')
        
        text_response(['бот жив', 'бот, ты жив', 'ты жив, бот'],
                      'Так точно, капитан')
        
        text_response(['утра', 'доброе утро', 'утречка'], 'utro.txt')
        
        text_response(['украин'], '🇺🇦')
        
        text_response(['рот ебал', 'ебал в рот'], 'Фуууу, противно!')

        text_response([r'\bага$'], 'в жопе нога', 33)

        text_response([r'\bнет$'], 'пидора ответ', 10)

    def reply_responses(self, bot, update):
        def reply_response(patterns, answer, chance=100):
            if any(re.search(pattern, text) for pattern in patterns):
                if answer.endswith('.txt'):
                    answer = self._choice_variant_from_file(answer)
            
                if randint(1, 100) <= chance:
                    bot.sendMessage(chat_id=chat_id, text=answer,
                                    reply_to_message_id=message_id,
                                    markdown_support=True)
    
        message = update.message
        chat_id = message.chat_id
        text = message.text.lower()
        message_id = message.message_id
    
        reply_response(['.*'], "Чё сказал?", 33)
    
    def _me(self, bot, update, args):
        message = update.message
        
        text = "{0} {1}".format(message.from_user.username, ' '.join(args))
        bot.sendMessage(chat_id=self._chat_id, text=text)

    @staticmethod
    def _choice_variant_from_file(file_name):
        with open('modules/responses/%s' % file_name) as file:
            variant = choice(file.read().splitlines())
        return variant
