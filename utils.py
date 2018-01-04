import supycache


@supycache.supycache(cache_key='admin_ids_{1}', max_age=10 * 60)
def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def is_user_group_admin(bot, user_id, chat_id_, admin_id):
    if chat_id_ == admin_id:
        return False
    return user_id in get_admin_ids(bot, chat_id_)
