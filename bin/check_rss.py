import feedparser
from dateutil import parser, tz
from telegram import Bot, ParseMode

from model import Feed
from settings import CHAT_ID, TOKEN

bot = Bot(TOKEN)

for feed in Feed.select():
    for entry in reversed(feedparser.parse(feed.url).entries):
        published = parser.parse(entry.published).astimezone(
            tz.tzutc()).replace(tzinfo=None)
        
        if published <= feed.last_update:
            continue

        bot.sendMessage(chat_id=CHAT_ID, parse_mode=ParseMode.MARKDOWN,
                        text='[{0}]({1})'.format(entry.title, entry.link),
                        disable_web_page_preview=True)
        feed.last_update = published
        feed.save()
