from aiogram import Dispatcher, types

from init_bot import bot
from data_base import sqlite_db
from inline_keyboards.buttons_for_users import keyboard_for_users


async def second_brand_samara_get(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Самара> и получение фотографии."""
    await bot.answer_callback_query(callback.id)
    await sqlite_db.sql_b2_samara_read(callback.message)


async def second_brand_dagestan_get(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Дагестан> и получение фотографии."""
    await bot.answer_callback_query(callback.id)
    await sqlite_db.sql_b2_dagestan_read(callback.message)


async def second_brand_exit_callback(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Назад> в списке магазинов второго бренда."""
    text = 'At which point of sale will we look at the design??'
    await bot.edit_message_text(text, chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_users(
                                    'outlets_open'))


def register_second_brand_handlers(dp: Dispatcher):
    """Регистрация хендлеров по работе со вторым брендом."""
    dp.register_callback_query_handler(second_brand_samara_get,
                                       text='sb_samara')
    dp.register_callback_query_handler(second_brand_dagestan_get,
                                       text='sb_dagestan')
    dp.register_callback_query_handler(second_brand_exit_callback,
                                       text='sb_back')