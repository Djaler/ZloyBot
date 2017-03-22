from peewee import Model, PrimaryKeyField

from model import database


class BaseEntity(Model):
    id = PrimaryKeyField()
    
    class Meta:
        database = database
