from peewee import *

from model.base_entity import BaseEntity


class BlockedStickerpack(BaseEntity):
    name = TextField()
    
    class Meta:
        db_table = 'blocked_stickerpacks'
