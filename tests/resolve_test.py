import unittest
from unittest.mock import MagicMock

from modules.resolve import resolve


class ResolveTestCase(unittest.TestCase):
    def setUp(self):
        self.chat_id = 1
        
        self.bot = MagicMock()
        self.update = MagicMock()
        self.update.message.message_id = 42
        self.update.message.chat_id = self.chat_id
    
    def test_random(self):
        variants = ['1', '2', '3']
        args = ['/', '/'.join(variants)]
        resolve(self.bot, self.update, args)
        for variant in variants:
            try:
                self.bot.sendMessage.assert_called_once_with(
                    chat_id=self.chat_id,
                    reply_to_message_id=self.update.message.message_id,
                    text=variant)
            except AssertionError:
                pass
            else:
                break
        else:
            try:
                self.bot.sendMessage.assert_called_once_with(
                    chat_id=self.chat_id,
                    reply_to_message_id=self.update.message.message_id,
                    text='Я откуда знаю? Отъебись')
            except AssertionError:
                raise AssertionError("Чет левый ответ какой-то пришел")
    
    def test_empty_variants(self):
        args = []
        resolve(self.bot, self.update, args)
        
        self.bot.sendMessage.assert_called_once_with(chat_id=self.chat_id,
                                                     reply_to_message_id=self.update.message.message_id,
                                                     text='Ну а где варианты?')
    
    def test_one_variant(self):
        variants = ['1', '1']
        args = ['/'.join(variants)]
        resolve(self.bot, self.update, args)
        
        self.bot.sendMessage.assert_called_once_with(chat_id=self.chat_id,
                                                     reply_to_message_id=self.update.message.message_id,
                                                     text='Эмм, тут так-то '
                                                          'один вариант...')
        
        variants = ['1']
        args = ['/'.join(variants)]
        resolve(self.bot, self.update, args)
        
        self.bot.sendMessage.assert_called_with(chat_id=self.chat_id,
                                                reply_to_message_id=self.update.message.message_id,
                                                text='Эмм, тут так-то '
                                                     'один вариант...')


if __name__ == '__main__':
    unittest.main()
