import re
from random import choice, randint, shuffle
from typing import Text, List, Union

from telegram.ext import CommandHandler, Filters, MessageHandler

from filters import reply_to_bot_filter
from utils import get_username_or_name


class PrimitiveResponse:
    def __init__(self, chat_id):
        self._chat_id = chat_id

    def add_handlers(self, add_handler):
        add_handler(MessageHandler(Filters.text | Filters.command, self.text_responses))
        add_handler(
            MessageHandler(Filters.text & reply_to_bot_filter,
                           self.reply_responses))
        add_handler(CommandHandler('me', self._me, pass_args=True))

    def text_responses(self, bot, update):
        class Response:
            def __init__(self, patterns, answer, chance):
                self.patterns = patterns
                self.answer = answer
                self.chance = chance

        def text_response(patterns, answer: Union[Text, List], chance=100):
            if isinstance(answer, list):
                answer = choice(answer)

            if answer.endswith('.txt'):
                answer = self._choice_variant_from_file(answer)

            responses.append(Response(patterns, answer, chance))

        responses = []
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

        text_response(['рот ебал', 'ебал в рот'], 'Фуууу, противно!')

        text_response(['не получается', 'не получилось'], 'ну ты и лох')

        text_response([r'\bага$'], 'в жопе нога', 33)

        text_response([r'\bнет$'], 'пидора ответ', 10)

        text_response(['/ban', r'\bban$'], ['себя забань', 'давно пора'], 50)

        shuffle(responses)

        for resp in responses:
            if any(re.search(pattern, text) for pattern in resp.patterns):
                if randint(1, 100) <= resp.chance:
                    bot.sendMessage(chat_id=chat_id, text=resp.answer,
                                    reply_to_message_id=message_id,
                                    markdown_support=True)
                    break

    def reply_responses(self, bot, update):
        def reply_response(patterns, answer: Union[Text, List], chance=100):
            if any(re.search(pattern, text) for pattern in patterns):
                if isinstance(answer, list):
                    answer = choice(answer)
                
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

        reply_response(['.*'], ["Чё сказал?", "А ну повтори", 'Слыш, пошли выйдем'], 50)

    def _me(self, bot, update, args):
        message = update.message

        text = "{0} {1}".format(get_username_or_name(message.from_user), ' '.join(args))
        bot.sendMessage(chat_id=self._chat_id, text=text)

    @staticmethod
    def _choice_variant_from_file(file_name):
        with open('modules/responses/%s' % file_name) as file:
            variant = choice(file.read().splitlines())
        return variant
