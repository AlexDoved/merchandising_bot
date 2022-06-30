import sqlite3 as sq

from init_bot import bot


def sql_start():
    """Подключение к БД и создание таблиц."""
    global base, cursor
    base = sq.connect('company.db')
    cursor = base.cursor()
    if base:
        print('Connected!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS outlets(img TEXT, name TEXT PRIMARY KEY, comment TEXT)')
    base.execute(
        'CREATE TABLE IF NOT EXISTS samples(doc TEXT, name TEXT PRIMARY KEY, month TEXT)')
    base.commit()


async def sql_add_command_sample(state):
    """Загрузка образца в БД."""
    async with state.proxy() as data:
        cursor.execute('INSERT INTO samples VALUES (?, ?, ?)',
                       tuple(data.values()))
        base.commit()


async def sql_add_command_outlet(state):
    """Загрузка магазина в БД."""
    async with state.proxy() as data:
        cursor.execute('INSERT INTO outlets VALUES (?, ?, ?)',
                       tuple(data.values()))
        base.commit()


async def sql_read_db_samples():
    """Чтение БД (таблица с образцами)."""
    return cursor.execute('SELECT * FROM samples').fetchall()


async def sql_read_db_outlets():
    """Чтение БД (таблица с магазинами)."""
    return cursor.execute('SELECT * FROM outlets').fetchall()


async def sql_delete_db_sample(data):
    """Удаление образца из БД."""
    cursor.execute('DELETE FROM samples WHERE name == ?', (data,))
    base.commit()


async def sql_delete_db_outlet(data):
    """Удаление магазина из БД."""
    cursor.execute('DELETE FROM outlets WHERE name == ?', (data,))
    base.commit()


async def sql_exist_name_outlet(message):
    """Проверка на наличие в БД наименования магазина."""
    name = message.upper()
    name_in_db = cursor.execute('SELECT name FROM outlets WHERE name = ?',
                                [name]).fetchone()
    return name_in_db


async def sql_exist_name_sample(message):
    """Проверка на наличие в БД наименования образца."""
    name = message.upper()
    name_in_db = cursor.execute('SELECT name FROM samples WHERE name = ?',
                                [name]).fetchone()
    return name_in_db


async def send_pdf_or_none_object(document, message):
    """Проверка на наличие объекта в БД, отправление ботом PDF-файла."""
    if document is None:
        await bot.send_message(message.chat.id,
                               'There is no such document in the database 🤷‍♂')
    else:
        await bot.send_document(message.chat.id, document[0],
                                caption=f'Name: <strong>{document[1]}</strong>\n'
                                        f'Month: <strong>{document[-1]}</strong>',
                                parse_mode='HTML')


async def sql_first_brand_doc_read(message):
    """Получение документа по названию <BRAND 1>."""
    document = cursor.execute(
        "SELECT * FROM samples WHERE name LIKE 'BRAND 1%'").fetchone()
    await send_pdf_or_none_object(document, message)


async def sql_second_brand_doc_read(message):
    """Получение документа по названию <BRAND 2>."""
    document = cursor.execute(
        "SELECT * FROM samples WHERE name LIKE 'BRAND 2%'").fetchone()
    await send_pdf_or_none_object(document, message)


async def send_photo_or_none_object(outlet, message):
    """Проверка на наличие объекта в БД, отправление ботом фотографии."""
    if outlet is None:
        await bot.send_message(message.chat.id,
                               'There is no photo from this outlet 🤷‍♂')
    else:
        await bot.send_photo(message.chat.id, outlet[0],
                             f'Name: <strong>{outlet[1]}</strong>\n'
                             f'Comment: {outlet[-1]}',
                             parse_mode='HTML')


async def sql_b1_moscow_read(message):
    """Получение фотографии по названию <Москва>."""
    outlet = cursor.execute(
        "SELECT * FROM outlets WHERE name LIKE 'MOSCOW%'").fetchone()
    await send_photo_or_none_object(outlet, message)


async def sql_b1_omsk_read(message):
    """Получение фотографии по названию <Омск>."""
    outlet = cursor.execute(
        "SELECT * FROM outlets WHERE name LIKE 'OMSK%'").fetchone()
    await send_photo_or_none_object(outlet, message)


async def sql_b2_samara_read(message):
    """Получение фотографии по названию <Самара>."""
    outlet = cursor.execute(
        "SELECT * FROM outlets WHERE name LIKE 'SAMARA%'").fetchone()
    await send_photo_or_none_object(outlet, message)


async def sql_b2_dagestan_read(message):
    """Получение фотографии по названию <Дагестан>."""
    outlet = cursor.execute(
        "SELECT * FROM outlets WHERE name LIKE 'DAGESTAN%'").fetchone()
    await send_photo_or_none_object(outlet, message)
