from aiogram import Dispatcher, types

from init_bot import bot
from exceptions import BotInteractionError
from inline_keyboards.buttons_for_users import keyboard_for_users


async def command_start_help(message: types.Message):
    """Справочная информация после команды /start или /help."""
    try:
        await bot.send_message(
            message.from_user.id,
            'Hello 👋\n''\n'
            'What I can do:''\n'
            '✔ send samples of product placement\n'
            'in PDF format''\n'
            '✔ send photos from retail outlets\n',
            reply_markup=await keyboard_for_users('start_keyboard'))
        await message.delete()
    except BotInteractionError:
        await message.reply(
            'I have to learn how to communicate with you in private messages, '
            'write to me:\n@alex_doved_telegram')


async def list_of_samples_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Получить образец>."""
    text = 'What document do you need?'
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'samples_open'))


async def list_of_samples_exit_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Назад> в списке брендов."""
    text = (f'Hello 👋\n\nWhat I can do:\n'
            f'✔ send samples of product placement\nin PDF format\n'
            f'✔ send photos from retail outlets\n')
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'start_keyboard'))


async def retail_outlets_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Получить фотографию>."""
    text = 'Where will we look at the design?'
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'outlets_open'))


async def retail_outlets_exit_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Назад> в списке точек."""
    text = (f'Hello 👋\n\nWhat I can do:\n'
            f'✔ send samples of product placement\nin PDF format\n'
            f'✔ send photos from retail outlets\n')
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'start_keyboard'))


async def first_brand_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Brand 1>."""
    text = "Which «Brand 1» outlet should I send you?"
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'first_brand_open'))


async def second_brand_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Brand 2>."""
    text = "Which «Brand 2» outlet should I send you?"
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'second_brand_open'))


def register_handlers_for_users(dp: Dispatcher):
    """Регистрация хендлеров для пользователей."""
    dp.register_message_handler(command_start_help, commands=['start', 'help'])
    dp.register_callback_query_handler(list_of_samples_callback,
                                       text='samples_doc')
    dp.register_callback_query_handler(list_of_samples_exit_callback,
                                       text='samples_back')
    dp.register_callback_query_handler(retail_outlets_callback,
                                       text='outlets_img')
    dp.register_callback_query_handler(retail_outlets_exit_callback,
                                       text='outlets_back')
    dp.register_callback_query_handler(first_brand_callback,
                                       text='fb_img')
    dp.register_callback_query_handler(second_brand_callback,
                                       text='sb_img')
