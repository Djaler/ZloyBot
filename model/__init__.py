import urllib.parse

from settings import DATABASE_URL, ENV

if ENV == "prod":
    from playhouse.pool import PooledPostgresqlDatabase

    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(DATABASE_URL)
    database = PooledPostgresqlDatabase(url.path[1:], user=url.username,
                                        password=url.password, host=url.hostname,
                                        port=url.port, max_connections=10,
                                        stale_timeout=30)
else:
    from peewee import SqliteDatabase

    database = SqliteDatabase(DATABASE_URL)

from model.user import User
from model.user_messages_info import UserMessagesInfo
from model.feed import Feed
from model.last_users import LastUsers
from model.blocked_stickerpack import BlockedStickerpack


def init_database():
    database.connect()
    database.create_tables(
        [User, UserMessagesInfo, Feed, LastUsers, BlockedStickerpack], True)
