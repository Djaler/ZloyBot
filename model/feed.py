from peewee import *

from model.base_entity import BaseEntity


class Feed(BaseEntity):
    url = TextField(unique=True)
    last_update = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    summary = BooleanField(default=False)
    preview = BooleanField(default=False)
    
    class Meta:
        db_table = 'feeds'
