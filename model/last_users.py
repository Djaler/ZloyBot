from peewee import *

from model.base_entity import BaseEntity
from model.user import User


class LastUsers(BaseEntity):
    user = ForeignKeyField(User)
    
    class Meta:
        db_table = 'last_users'
