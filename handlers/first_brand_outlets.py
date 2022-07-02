from aiogram import Dispatcher, types

from init_bot import bot
from data_base import sqlite_db
from inline_keyboards.buttons_for_users import keyboard_for_users


async def first_brand_moscow_get(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Москва> и получение фотографии."""
    await bot.answer_callback_query(callback.id)
    await sqlite_db.sql_b1_moscow_read(callback.message)


async def first_brand_omsk_get(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Омск> и получение фотографии."""
    await bot.answer_callback_query(callback.id)
    await sqlite_db.sql_b1_omsk_read(callback.message)


async def first_brand_exit_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Назад> в списке магазинов первого бренда."""
    text = 'In which store will we look at the design?'
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'outlets_open'))


def register_first_brand_handlers(dp: Dispatcher):
    """Регистрация хендлеров по работе с первым брендом."""
    dp.register_callback_query_handler(first_brand_moscow_get,
                                       text='fb_moscow')
    dp.register_callback_query_handler(first_brand_omsk_get,
                                       text='fb_omsk')
    dp.register_callback_query_handler(first_brand_exit_callback,
                                       text='fb_back')
