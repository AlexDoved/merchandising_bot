from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from init_bot import bot
from data_base import sqlite_db
from inline_keyboards.buttons_for_admins import keyboard_for_admins
from inline_keyboards.buttons_for_users import keyboard_for_users
from keyboards import kb_cancel_sample

ID = None
sample_names = ('BRAND 1', 'BRAND 2')

months_list = (
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December')


class DocumentPDF(StatesGroup):
    document = State()
    name = State()
    month = State()


async def sample_admin_command(message: types.Message):
    """От админа поступила команда по началу работы с документами."""
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id,
                           'The mode of the administrator of design samples.',
                           reply_markup=await keyboard_for_admins(
                               'admin_load_sample'))
    await message.delete()


async def open_main_samples_func_callback(callback: types.CallbackQuery):
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


async def add_sample_callback(callback: types.CallbackQuery):
    """Запускается машина состояний по загрузке документа в БД."""
    if callback.from_user.id == ID:
        await DocumentPDF.document.set()
        await bot.answer_callback_query(callback.id)
        await callback.message.reply(
            'Upload the <strong>PDF file</strong> 👉📎',
            reply_markup=kb_cancel_sample,
            parse_mode='HTML')


async def sample_cancel_handler(message: types.Message, state: FSMContext):
    """Отмена загрузки документа в БД."""
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.answer('<strong>Adding a document is canceled! 👌</strong>',
                             reply_markup=types.ReplyKeyboardRemove(),
                             parse_mode='HTML')
    await message.delete()


async def sample_load_document(message: types.Message, state: FSMContext):
    """Загрузка документа, ожидание следующего ответа."""
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['document'] = message.document.file_id
        await DocumentPDF.next()
        await message.reply('Enter <strong>the '
                            'name</strong> of the document 📝',
                            parse_mode='HTML')


async def sample_load_name(message: types.Message, state: FSMContext):
    """Загрузка имени документа, ожидание следующего ответа."""
    if message.from_user.id == ID:
        admin_message = message.text.upper()
        async with state.proxy() as data:
            if admin_message not in sample_names:
                await message.reply('Enter the correct name!',
                                    reply_markup=await keyboard_for_admins(
                                        'admin_help_name_sample'))
            else:
                if (
                        await sqlite_db.sql_exist_name_sample(
                            message.text)) is None:
                    data['name'] = message.text.upper()
                    await DocumentPDF.next()
                    await message.reply(
                        'Enter <strong>the name</strong> of the month 🌙',
                        parse_mode='HTML'
                    )
                else:
                    await message.reply(
                        'There is already such an object in the database, '
                        'delete the old one!'
                        'And try again!'
                    )


async def help_sample_callback(callback: types.CallbackQuery):
    """Вывод списка доступных названий документов в виде подсказки."""
    text = '🔹'.join(list(sample_names))
    await bot.edit_message_text(str(text), chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_admins(
                                    'help_name_sample_exit'))


async def help_sample_callback_exit(callback: types.CallbackQuery):
    """Сворачивание подсказки <название документа>."""
    text = 'Enter <strong>the name</strong> of the document 📝'
    await bot.edit_message_text(str(text), chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_admins(
                                    'admin_help_name_merch'),
                                parse_mode='HTML')


async def help_month_callback(callback: types.CallbackQuery):
    """Вывод списка доступных месяцев в виде подсказки."""
    text = '🔹'.join(list(months_list))
    await bot.edit_message_text(str(text), chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_admins(
                                    'help_name_month_exit'))


async def help_month_callback_exit(callback: types.CallbackQuery):
    """Сворачивание подсказки <название месяца>."""
    text = 'Enter the correct name of the month!'
    await bot.edit_message_text(str(text), chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=await keyboard_for_admins(
                                    'admin_help_name_month'),
                                parse_mode='HTML')


async def sample_load_month(message: types.Message, state: FSMContext):
    """Загрузка названия месяца, использование всех полученных данных."""
    if message.from_user.id == ID:
        admin_message = message.text.capitalize()
        if admin_message not in months_list:
            await message.reply('Enter the correct name of the month!',
                                reply_markup=await keyboard_for_admins(
                                    'admin_help_name_month'))
        else:
            async with state.proxy() as data:
                data['month'] = message.text.capitalize()
            await sqlite_db.sql_add_command_sample(state)
            await message.answer(
                '☑ <strong>The object was successfully added to the '
                'database!</strong> ☑',
                reply_markup=types.ReplyKeyboardRemove(),
                parse_mode='HTML')
            await bot.send_message(message.from_user.id,
                                   text="Don't forget to clear the chat "
                                        "history manually! 💨",
                                   reply_markup=await keyboard_for_admins(
                                       'admin_load_sample'))
            await state.finish()


async def delete_sample_callback_run(callback: types.CallbackQuery):
    """Выбор объекта (документы) и подтверждение его удаления из БД."""
    await sqlite_db.sql_delete_db_sample(callback.data.replace('del ', ''))
    await callback.answer(
        text=f'{callback.data.replace("del ", "")} deleted.',
        show_alert=True)


async def delete_sample_callback(callback: types.CallbackQuery):
    """Получение админом объектов (документов) для удаления из БД."""
    await bot.answer_callback_query(callback.id)
    if callback.from_user.id == ID:
        read_db = await sqlite_db.sql_read_db_samples()
        for sample in read_db:
            await bot.send_document(callback.from_user.id, sample[0],
                                    caption=f'Name: {sample[1]}\n'
                                            f'Relevance of '
                                            f'the document: {sample[-1]}')
            await bot.send_message(callback.from_user.id, text='🔺🔺🔺',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(
                                           f'Remove {sample[1]}',
                                           callback_data=f'del {sample[1]}')))
        await bot.send_message(callback.from_user.id,
                               text="⬆ This is the last document, "
                                    "unloaded from the database.\n"
                                    "Don't forget to clean "
                                    "your chat history manually 💨",
                               reply_markup=await keyboard_for_admins(
                                   'admin_load_sample'),
                               parse_mode='HTML')


def register_handlers_admin_samples(dp: Dispatcher):
    """Регистрация хендлеров по работе с документами."""
    dp.register_message_handler(sample_admin_command, commands=['edit_sample'],
                                is_chat_admin=True)
    dp.register_callback_query_handler(add_sample_callback,
                                       lambda x: x.data == 'load_pdf',
                                       state=None)
    dp.register_message_handler(sample_cancel_handler, state='*',
                                commands='cancel-pdf')
    dp.register_message_handler(sample_load_document,
                                content_types=['document'],
                                state=DocumentPDF.document)
    dp.register_message_handler(sample_load_name, state=DocumentPDF.name)
    dp.register_message_handler(sample_load_month, state=DocumentPDF.month)
    dp.register_callback_query_handler(open_main_samples_func_callback,
                                       lambda x: x.data == 'main_func_sample')
    dp.register_callback_query_handler(delete_sample_callback,
                                       lambda x: x.data == 'delete_pdf')
    dp.register_callback_query_handler(delete_sample_callback_run,
                                       lambda x: x.data and x.data.startswith(
                                           'del '))
    dp.register_callback_query_handler(help_sample_callback,
                                       text='help_sample', state='*')
    dp.register_callback_query_handler(help_sample_callback_exit,
                                       text='help_sample_back', state='*')
    dp.register_callback_query_handler(help_month_callback,
                                       text='help_month', state='*')
    dp.register_callback_query_handler(help_month_callback_exit,
                                       text='help_month_back', state='*')
