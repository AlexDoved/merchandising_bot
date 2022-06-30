import os

from aiogram import Dispatcher, types
from dotenv import load_dotenv

from init_bot import bot
from handlers.handlers_for_users import command_start_help
from handlers.additional_handlers import bad_words_filter

ID = None

load_dotenv()
users = tuple(map(int, (os.getenv('USERS')).split(', ')))
commands = ('/start', '/help')


async def private_bot(message: types.Message):
    """
    Проверка id пользователей, которым разрешен доступ к боту.
    Проверка сообщений в чате, чтобы бот среагировал на команды.
    """
    if message.from_user.id not in users:
        for command in commands:
            if str(message.text) in command:
                await message.delete()
                await bot.send_message(
                    message.from_user.id,
                    "You don't have access!"
                )
    else:
        await bad_words_filter(message)
        for command in commands:
            if str(message.text) in command:
                await command_start_help(message)


def register_access_bot_handler(dp: Dispatcher):
    """Регистрация хендлера с проверкой доступа к боту."""
    dp.register_message_handler(private_bot)
