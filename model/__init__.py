import os
import urllib.parse

from peewee import PostgresqlDatabase

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
database = PostgresqlDatabase(url.path[1:], user=url.username,
                              password=url.password, host=url.hostname,
                              port=url.port)

from model.user import User
from model.user_messages_info import UserMessagesInfo


def init_database():
    database.connect()
    database.create_tables(
        [User, UserMessagesInfo], True)
