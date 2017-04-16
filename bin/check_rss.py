import re

import feedparser
from dateutil import parser, tz
from telegram import Bot, ParseMode

from model import Feed
from settings import CHAT_ID, TOKEN


def delete_unsupported_html_tags(text):
    return re.sub(r'<(?!/?(b|i|a|code|pre)\b).*?>', "", text)


bot = Bot(TOKEN)

for feed in Feed.select():
    for entry in reversed(feedparser.parse(feed.url).entries):
        published = parser.parse(entry.published).astimezone(
            tz.tzutc()).replace(tzinfo=None)
        
        if published <= feed.last_update:
            continue

        text = '<a href="{}">{}</a>'.format(entry.link, entry.title)

        if feed.summary:
            text += "\n"
            text += delete_unsupported_html_tags(entry.summary)

        bot.send_message(chat_id=CHAT_ID, parse_mode=ParseMode.HTML,
                         text=text,
                         disable_web_page_preview=True)
        feed.last_update = published
        feed.save()
