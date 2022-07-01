from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from init_bot import bot
from data_base import sqlite_db
from inline_keyboards.buttons_for_admins import keyboard_for_admins
from inline_keyboards.buttons_for_users import keyboard_for_users
from keyboards import kb_cancel

ID = None
store_names = ('MOSCOW', 'OMSK', 'SAMARA', 'DAGESTAN')


class RetailOutletAdmin(StatesGroup):
    photo = State()
    name = State()
    comment = State()


async def outlet_admin_command(message: types.Message):
    """От админа поступила команда по началу работы с точками."""
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id,
                           'The mode of the administrator of retail outlets.',
                           reply_markup=await keyboard_for_admins(
                               'admin_load_outlet'))
    await message.delete()


async def open_main_outlets_func_callback(callback: types.CallbackQuery):
    """Открываются основные функции бота."""
    if callback.from_user.id == ID:
        await bot.answer_callback_query(callback.id)
        await bot.send_message(
            callback.from_user.id,
            'Hello 👋\n''\n'
            'What I can do:''\n'
            '✔ send samples of product placement\n'
            'in PDF format''\n'
            '✔ send photos from retail outlets\n',
            reply_markup=await keyboard_for_users('start_keyboard'))


async def add_outlet_callback(callback: types.CallbackQuery):
    """Запускается машина состояний по загрузке точки в БД."""
    if callback.from_user.id == ID:
        await RetailOutletAdmin.photo.set()
        await bot.answer_callback_query(callback.id)
        await bot.send_message(callback.from_user.id,
                               text='Upload a <strong>photo</strong> 👉📎',
                               reply_markup=kb_cancel, parse_mode='HTML')


async def outlet_cancel_handler(message: types.Message, state: FSMContext):
    """Отмена загрузки точки в БД."""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('<strong>The upload to the '
                             'database was canceled! 👌</strong>',
                             reply_markup=types.ReplyKeyboardRemove(),
                             parse_mode='HTML')
    await message.delete()


async def outlet_load_photo(message: types.Message, state: FSMContext):
    """Загрузка фотографии, ожидание следующего ответа."""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await RetailOutletAdmin.next()
        await message.reply('Enter the <strong>name</strong> of the outlet 📝',
                            parse_mode='HTML')


async def outlet_load_name(message: types.Message, state: FSMContext):
    """Загрузка названия точки, ожидание следующего ответа."""
    if message.from_user.id == ID:
        admin_message = message.text.upper()
        async with state.proxy() as data:
            if admin_message not in store_names:
                await message.reply('Enter the correct name!',
                                    reply_markup=await keyboard_for_admins(
                                        'admin_help_name_outlet'))
            else:
                if (
                        await sqlite_db.sql_exist_name_outlet(
                            message.text)) is None:
                    data['name'] = message.text.upper()
                    await RetailOutletAdmin.next()
                    await message.reply(
                        'Leave a <strong>comment</strong> ✏',
                        parse_mode='HTML'
                    )
                else:
                    await message.reply(
                        'There is already such an object in the database, '
                        'delete the old one!'
                        'And try again!'
                    )


async def help_outlet_callback(callback: types.CallbackQuery):
    """Вывод списка доступных названий точек в виде подсказки."""
    text = '🔹'.join(list(store_names))
    await bot.edit_message_text(str(text), chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_admins(
                                    'help_name_outlet_exit'))


async def help_outlet_callback_exit(callback: types.CallbackQuery):
    """Сворачивание подсказки."""
    text = 'Enter the <strong>name</strong> of the outlet 📝'
    await bot.edit_message_text(str(text), chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_admins(
                                    'admin_help_name_outlet'),
                                parse_mode='HTML')


async def outlet_load_comment(message: types.Message, state: FSMContext):
    """Загрузка комментария, использование всех полученных данных."""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['comment'] = message.text
        await sqlite_db.sql_add_command_outlet(state)
        await message.answer(
            '☑ <strong>The object was successfully added to the '
            'database!</strong> ☑',
            reply_markup=types.ReplyKeyboardRemove(),
            parse_mode='HTML')
        await bot.send_message(message.from_user.id,
                               text="Don't forget to clear the chat "
                                    "history manually! 💨",
                               reply_markup=await keyboard_for_admins(
                                   'admin_load_outlet'))
        await state.finish()


async def delete_outlet_callback_run(callback: types.CallbackQuery):
    """Выбор объекта (точки) и подтверждение его удаления из БД."""
    await sqlite_db.sql_delete_db_outlet(callback.data.replace('delete ', ''))
    await callback.answer(
        text=f'{callback.data.replace("delete ", "")} deleted.',
        show_alert=True)


async def delete_outlet_callback(callback: types.CallbackQuery):
    """Получение админом объектов (точек) для удаления из БД."""
    await bot.answer_callback_query(callback.id)
    if callback.from_user.id == ID:
        read_db = await sqlite_db.sql_read_db_outlets()
        for point in read_db:
            await bot.send_photo(callback.from_user.id, point[0],
                                 f'Name: {point[1]}\nComment: {point[-1]}')
            await bot.send_message(callback.from_user.id, text='🔺🔺🔺',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(
                                           f'Remove {point[1]}',
                                           callback_data=f'delete {point[1]}')))
        await bot.send_message(callback.from_user.id,
                               text="<strong>⬆ This is the last point of sale, "
                                    "unloaded from the database.\n"
                                    "Don't forget to clean "
                                    "your chat history manually 💨",
                               reply_markup=await keyboard_for_admins(
                                   'admin_load_outlet'),
                               parse_mode='HTML')


def register_handlers_admin_outlets(dp: Dispatcher):
    """Регистрация хендлеров по работе с точками."""
    dp.register_message_handler(outlet_admin_command, commands=['edit_outlet'],
                                is_chat_admin=True)
    dp.register_callback_query_handler(add_outlet_callback,
                                       lambda x: x.data == 'load_outlet',
                                       state=None)
    dp.register_message_handler(outlet_cancel_handler, state='*',
                                commands='cancel')
    dp.register_message_handler(outlet_load_photo, content_types=['photo'],
                                state=RetailOutletAdmin.photo)
    dp.register_message_handler(outlet_load_name, state=RetailOutletAdmin.name)
    dp.register_message_handler(outlet_load_comment, state=RetailOutletAdmin.comment)
    dp.register_callback_query_handler(open_main_outlets_func_callback,
                                       lambda x: x.data == 'main_func_outlet')
    dp.register_callback_query_handler(delete_outlet_callback,
                                       lambda x: x.data == 'delete_outlet')
    dp.register_callback_query_handler(delete_outlet_callback_run,
                                       lambda x: x.data and x.data.startswith(
                                           'delete '))
    dp.register_callback_query_handler(help_outlet_callback,
                                       text='help_outlet', state='*')
    dp.register_callback_query_handler(help_outlet_callback_exit,
                                       text='help_outlet_back', state='*')
