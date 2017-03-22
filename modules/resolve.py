import random
import re


def resolve(bot, update, args):
    message = update.message
    
    variants = set(re.split(' */ *', ' '.join(args)))
    variants.discard('')
    variants = list(variants)
    if not variants:
        bot.sendMessage(chat_id=message.chat_id,
                        reply_to_message_id=message.message_id,
                        text='Ну а где варианты?')
        return
    
    if len(variants) == 1:
        bot.sendMessage(chat_id=message.chat_id,
                        reply_to_message_id=message.message_id,
                        text='Эмм, тут так-то один вариант...')
        return
    elif random.randint(0, 100) == 0:
        bot.sendMessage(chat_id=message.chat_id,
                        reply_to_message_id=message.message_id,
                        text='Я откуда знаю? Отъебись')
        return
    
    bot.sendMessage(chat_id=message.chat_id,
                    reply_to_message_id=message.message_id,
                    text=random.choice(variants))
