import unittest
from unittest.mock import MagicMock

from modules.forward import Forward


class ForwardTestCase(unittest.TestCase):
    def setUp(self):
        self.chat_id = 1
        self.admin_id = 2
        self.moderators_ids = (self.admin_id,) + (3, 4)
        self.another_chat_id = 0
        self.another_chat_title = 'title'
        self.forward = Forward(self.chat_id, self.admin_id)
        
        self.bot = MagicMock()
        self.update = MagicMock()
        self.update.message.message_id = 42
    
    def test_message_from_main_chat(self):
        self.update.message.chat_id = self.chat_id
        
        self.forward._forward(self.bot, self.update)
        
        self.bot.forwardMessage.assert_not_called()
        self.bot.sendMessage.assert_not_called()
    
    def test_message_from_another_group_chat(self):
        self.update.message.chat_id = self.another_chat_id
        self.update.message.chat.title = self.another_chat_title
        self.update.message.chat.type = 'group'
        
        self.forward._forward(self.bot, self.update)
        self.bot.forwardMessage.assert_called_once_with(
            message_id=self.update.message.message_id,
            from_chat_id=self.update.message.chat_id, chat_id=self.admin_id)
        
        text = 'chat_id = {0}\ntitle = {1}'.format(self.another_chat_id,
                                                   self.another_chat_title)
        self.bot.sendMessage.assert_any_call(chat_id=self.admin_id, text=text)
    
    def test_message_from_another_private_chat(self):
        self.update.message.chat_id = self.another_chat_id
        self.update.message.chat.type = 'private'
        self.update.message.chat.title = None
        
        self.forward._forward(self.bot, self.update)
        self.bot.forwardMessage.assert_called_once_with(
            message_id=self.update.message.message_id,
            from_chat_id=self.update.message.chat_id, chat_id=self.admin_id)
        
        text = 'chat_id = {0}'.format(self.another_chat_id)
        
        self.bot.sendMessage.assert_called_once_with(chat_id=self.admin_id,
                                                     text=text)


if __name__ == '__main__':
    unittest.main()
