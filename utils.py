import supycache


@supycache.supycache(cache_key='admin_ids_{1}', max_age=10 * 60)
def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
