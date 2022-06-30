from aiogram import Dispatcher, types

from init_bot import bot
from data_base import sqlite_db


async def first_brand_document_get(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Brand 1> и получение PDF-файла."""
    await bot.answer_callback_query(callback.id)
    await sqlite_db.sql_first_brand_doc_read(callback.message)


async def second_brand_document_get(callback: types.CallbackQuery):
    """Нажатие инлайн-кнопки <Brand 2> и получение PDF-файла."""
    await bot.answer_callback_query(callback.id)
    await sqlite_db.sql_second_brand_doc_read(callback.message)


def register_document_handlers_client(dp: Dispatcher):
    """Регистрация хендлеров по работе с документами."""
    dp.register_callback_query_handler(first_brand_document_get,
                                       text='doc_brand_1')
    dp.register_callback_query_handler(second_brand_document_get,
                                       text='doc_brand_2')
