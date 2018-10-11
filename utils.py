import functools
import typing
import inspect
import itertools

import supycache
from telegram import Bot, User


@supycache.supycache(cache_key='admin_ids_{1}', max_age=10 * 60)
def get_admin_ids(bot: Bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def is_user_group_admin(bot: Bot, user_id, chat_id_, admin_id):
    if chat_id_ == admin_id:
        return False
    return user_id in get_admin_ids(bot, chat_id_)


def get_username_or_name(user: User):
    if user.username:
        return user.username
    if user.last_name:
        return '%s %s' % (user.first_name, user.last_name)
    return user.first_name


def parse_callback_data(data: str) -> typing.Tuple[str, str]:
    module, data = data.split('/', maxsplit=1)
    return module, data


def get_callback_data(data: str) -> str:
    module, data = parse_callback_data(data)
    return data


def set_callback_data(data: str) -> str:
    """
    Хелпер, который добавляет в строку название модуля из которого выполняется.
    Необходим, чтобы потом понимать каким хендлером обрабатывать CallbackQuery.
    """

    module = inspect.currentframe().f_back.f_globals['__name__'].split('.')[-1]
    return f'{module}/{data}'


def process_callback_query(func):
    """Позволяет выполнять CallbackQueryHandler только из того модуля, который находится в callback_data"""

    current_module = inspect.currentframe().f_back.f_globals['__name__'].split('.')[-1]

    @functools.wraps(func)
    def inner(instance, bot, update):
        module, data = parse_callback_data(update.callback_query.data)
        if module == current_module:
            return func(instance, bot, update)
        return lambda: True  # помечает update с CallbackQuery обработанным, если ни один из хендлеров не подошел

    return inner


def grouper(iterable, n):
    """
    Позволяет разбивать итерабельный обьект по группам размера n

    В отличии от рецепта grouper(iterable, n, fillvalue=None) документации
    itertools (https://docs.python.org/3/library/itertools.html#itertools-recipes)
    не заполняет недостяющее количество элементов в группе при помощи fillvalue

    Возвращает генератор

    Пример:

    >>> my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> tuple(grouper(my_list, 3))
    ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    >>> tuple(grouper(my_list, 6))
    ((1, 2, 3, 4, 5, 6), (7, 8, 9))

    """
    it = iter(iterable)

    while True:
        res = tuple(itertools.islice(it, n))
        if res:
            yield res
        else:
            break