import random


def pay_respect(bot, update):
    message = update.message

    if message.reply_to_message:
        bot.send_sticker(message.chat_id, random.choice(_stickers),
                         reply_to_message_id=message.reply_to_message.message_id)
    else:
        bot.send_sticker(message.chat_id, random.choice(_stickers))


_stickers = [
    "CAADAgADrwADTptkAoftMsdli6fnAg",
    "CAADAgADsAADTptkAler0GVnHyzGAg",
    "CAADAgADsQADTptkArn64mdXYXbAAg",
    "CAADAgADsgADTptkAm1WnTBWvUfiAg",
    "CAADAgADswADTptkAs5hkxBiRE31Ag",
    "CAADAgADtAADTptkAq_OQoYz8ctCAg",
    "CAADAgADtQADTptkArZTqYEv5ofdAg",
    "CAADAgADtgADTptkAqpNYvdldSrYAg",
    "CAADAgADtwADTptkArfi9m2SDIPXAg",
    "CAADAgADuAADTptkAuKvD_a2Ho0nAg",
    "CAADAgADuQADTptkAn3O94Pvp3dmAg",
    "CAADAgADugADTptkArbrc3oLzTyHAg",
    "CAADAgADuwADTptkAk0zTSnOuax8Ag",
    "CAADAgAD2QADTptkAr_7hXFDc9mvAg",
    "CAADAgAD2gADTptkAupGXP51-SA0Ag",
    "CAADAgAD2wADTptkAje9NtoyOUz5Ag",
    "CAADAgAD3AADTptkAgABXf0bsR3XLAI",
    "CAADAgAD3QADTptkAsbfbuRgzncfAg",
    "CAADAgADCwEAAk6bZAKGibEPCbcdaQI",
    "CAADAgADDAEAAk6bZAJjkqwbNCLTRwI",
    "CAADAgADGwEAAk6bZAIif48xqmneWAI",
    "CAADAgADHAEAAk6bZAJeYSwNkVCdrAI",
    "CAADAgADHQEAAk6bZAJ6H3tM82FMtgI",
    "CAADAgADHgEAAk6bZAKj35UNnCMgCAI",
    "CAADAgADHwEAAk6bZALxgGJ9ZG8_2gI",
    "CAADAgADIAEAAk6bZAIGFAdo94ymKQI",
    "CAADAgADIQEAAk6bZALsWBeowE7nMwI",
    "CAADAgADIgEAAk6bZAJyyknLGt-gXQI",
    "CAADAgADIwEAAk6bZAK9Vjb4_T8KwgI",
    "CAADAgADJAEAAk6bZAIK9a8rwqx7TQI",
    "CAADAgADJQEAAk6bZALF7bI4ZKKKkAI",
    "CAADAgADJgEAAk6bZAKk4iM6sIcPrwI",
    "CAADAgADJwEAAk6bZAIlsD_1w-OfOAI",
    "CAADAgADKAEAAk6bZAKZ9J-Sevw3ZQI",
    "CAADAgADKQEAAk6bZAJ_ILxRYPzc6wI",
    "CAADAgADKgEAAk6bZAIx8zNIoA9ETwI",
    "CAADAgADKwEAAk6bZALaTCs_V_cERQI",
    "CAADAgADLAEAAk6bZAKtrgSyGwABdfwC",
    "CAADAgADLQEAAk6bZALto8-z5R4LPwI",
    "CAADAgADLgEAAk6bZAKPM2DZ2IZ3KAI",
    "CAADAgADLwEAAk6bZAKoAiUNs1BKsAI",
    "CAADAgADSAEAAk6bZAL7-VvSEK3IGQI",
    "CAADAgADSQEAAk6bZAJoKew9jTwM_gI",
    "CAADAgADSgEAAk6bZAI3xdjtSHj4UQI",
    "CAADAgADSwEAAk6bZAJh_WzbuQbfBAI",
    "CAADAgADTAEAAk6bZAIj7Q_wSl-eZgI",
    "CAADAgADTQEAAk6bZAI93BQQgHFr9QI",
    "CAADAgADTgEAAk6bZAK1iN90QqQ1WwI",
    "CAADAgADTwEAAk6bZAJ1Eu7R-LNOGgI",
    "CAADAgADUAEAAk6bZAJS9rHN7fKjYAI",
    "CAADAgADUQEAAk6bZAIytbpP3zso9wI",
    "CAADAgADUgEAAk6bZAKEtURpunKwrgI",
    "CAADAgADUwEAAk6bZAIaxDzKEZKWUQI",
    "CAADAgADVAEAAk6bZAKIX8hX1c_u3AI",
    "CAADAgADVQEAAk6bZALEUef8_bPn1gI",
    "CAADAgADVgEAAk6bZAL8mDV8bla2VQI",
    "CAADAgADVwEAAk6bZAIy_AfSMmh4fwI",
    "CAADAgADWAEAAk6bZALdMiXKucnqvwI",
    "CAADAgADWQEAAk6bZAIMOnpSqkvAjgI",
    "CAADAgADWgEAAk6bZAK5eeq_iFPbyAI",
    "CAADAgADWwEAAk6bZAKfvpp3HJ3EcgI",
    "CAADAgADXAEAAk6bZALSOXnDLsKNtQI",
    "CAADAgADXQEAAk6bZAJMcFKI-kEvSgI"
]
