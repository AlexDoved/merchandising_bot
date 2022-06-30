import json
import string

from aiogram import Dispatcher, types

from init_bot import bot


async def bad_words_filter(message: types.Message):
    """Фильтр матных и грубых слов."""
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.text.split()}.intersection(
        set(json.load(open('bad_words.json')))):
        await bot.send_message(message.from_user.id,
                               'Foul language is prohibited! 🤬')
        await message.delete()


def register_additional_handlers(dp: Dispatcher):
    """Регистрация дополнительных хендлеров."""
    dp.register_message_handler(bad_words_filter)