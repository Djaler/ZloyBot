import urllib.parse

from settings import DATABASE_URL, ENV

if ENV == "prod":
    from peewee import PostgresqlDatabase
    
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(DATABASE_URL)
    database = PostgresqlDatabase(url.path[1:], user=url.username,
                                  password=url.password, host=url.hostname,
                                  port=url.port)
else:
    from peewee import SqliteDatabase
    
    database = SqliteDatabase(DATABASE_URL)

from model.user import User
from model.user_messages_info import UserMessagesInfo
from model.feed import Feed


def init_database():
    database.connect()
    database.create_tables(
        [User, UserMessagesInfo, Feed], True)
