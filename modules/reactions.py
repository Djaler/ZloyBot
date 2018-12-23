import re
import random
from typing import List, Dict
from glob import glob

from telegram.ext import Filters, MessageHandler

from filters import reply_to_bot_filter
from validators import ReactionSchema


class Reactions:
    def __init__(self, chat_id):
        self._chat_id = chat_id

        self._reactions = self.load_reactions()

    @staticmethod
    def load_reactions() -> List[Dict]:
        """
        Загружает реакции из файлов по пути resources/reactions/ с именем *.json

        Бэкслэши в файлах должны быть экранированы (напр., \b -> \\b)

        Структура файла описана в классе ReactionsSchema в validators.py
        """
        reactions_files = glob(r'resources/reactions/*.json')
        schema = ReactionSchema(many=True)
        reactions: List[Dict] = []
        for file in reactions_files:
            with open(file, encoding='utf-8') as f:
                validated_data = schema.loads(f.read())
                if validated_data.errors:
                    print(f'Файл "{f.name}" содержит ошибки:', validated_data.errors)
                reactions += validated_data.data
        return reactions

    def add_handlers(self, add_handler) -> None:
        add_handler(MessageHandler(Filters.text | Filters.command, self.message_handler))

    def message_handler(self, bot, update) -> None:
        """
        Сообщение проверяется на соответствие с каждой загруженной реакцией.

        Для каждой реакции шанс просчитывается отдельно и не зависит от количества триггеров.

        Если реакция предназначена лишь на ответ боту - для обычных сообщений она будет пропущена.

        Из всех реакций, которые срабоатли на сообщение - случайным образом выбирается лишь одна.
        """
        message = update.message
        is_message_reply_to_bot: bool = reply_to_bot_filter.filter(message)

        # Каждый раз перемешиваем список реакций, затем
        # отправляем первое попавшееся совпадение
        random.shuffle(self._reactions)
        for reaction in self._reactions:
            chance: int = reaction['chance']
            if random.uniform(0, 100) > chance:
                continue

            if reaction['is_reply_to_bot'] and not is_message_reply_to_bot:
                continue

            if reaction['triggers']:
                for trigger in reaction['triggers']:
                    if re.search(trigger, message.text, re.IGNORECASE):
                        random_reaction = random.choice(reaction['reactions'])
                        return message.reply_text(random_reaction)
            else:
                random_reaction = random.choice(reaction['reactions'])
                return message.reply_text(random_reaction)
