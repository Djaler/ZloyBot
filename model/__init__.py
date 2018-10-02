import urllib.parse

from settings import DATABASE_URL, ENV, MAX_CONNECTIONS, STALE_TIMEOUT

if ENV == "prod":
    from playhouse.pool import PooledPostgresqlDatabase

    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(DATABASE_URL)
    database = PooledPostgresqlDatabase(url.path[1:], user=url.username,
                                        password=url.password, host=url.hostname,
                                        port=url.port, max_connections=MAX_CONNECTIONS,
                                        stale_timeout=STALE_TIMEOUT)
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
        [User, UserMessagesInfo, Feed, LastUsers, BlockedStickerpack])
