from peewee import *

from model.base_entity import BaseEntity
from model.user import User


class UserMessagesInfo(BaseEntity):
    user = ForeignKeyField(User, related_name='user_messages_info')
    number = IntegerField()
    
    class Meta:
        db_table = 'user_messages_info'
