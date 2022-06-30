from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def keyboard_for_admins(data):
    """Создание инлайн-клавиатуры для админа."""
    global keyboard_for_admins
    if data == 'admin_load_sample':
        menu_btn1 = InlineKeyboardButton('Upload a sample to the database  ✅',
                                         callback_data='load_pdf')
        menu_btn2 = InlineKeyboardButton('Delete a sample from the database  ❌',
                                         callback_data='delete_pdf')
        menu_btn3 = InlineKeyboardButton('The main functions of the bot  💎',
                                         callback_data='main_func_sample')
        keyboard_for_admins = InlineKeyboardMarkup().add(
            menu_btn3).add(
            menu_btn1).add(
            menu_btn2)

    elif data == 'admin_load_outlet':
        menu_btn1 = InlineKeyboardButton('Upload the point of sale to the database  ✅',
                                         callback_data='load_outlet')
        menu_btn2 = InlineKeyboardButton('Delete a point of sale from the database  ❌',
                                         callback_data='delete_outlet')
        menu_btn3 = InlineKeyboardButton('The main functions of the bot  💎',
                                         callback_data='main_func_outlet')
        keyboard_for_admins = InlineKeyboardMarkup().add(
            menu_btn3).add(
            menu_btn1).add(
            menu_btn2)

    elif data == 'admin_help_name_outlet':
        menu_btn1 = InlineKeyboardButton('Hint',
                                         callback_data='help_outlet')
        keyboard_for_admins = InlineKeyboardMarkup().add(menu_btn1)

    elif data == 'admin_help_name_sample':
        menu_btn1 = InlineKeyboardButton('Hint',
                                         callback_data='help_sample')
        keyboard_for_admins = InlineKeyboardMarkup().add(menu_btn1)

    elif data == 'admin_help_name_month':
        menu_btn1 = InlineKeyboardButton('Hint',
                                         callback_data='help_month')
        keyboard_for_admins = InlineKeyboardMarkup().add(menu_btn1)

    elif data == 'help_name_sample_exit':
        menu_btn1 = InlineKeyboardButton('Close the hint',
                                         callback_data='help_sample_back')
        keyboard_for_admins = InlineKeyboardMarkup().add(menu_btn1)

    elif data == 'help_name_outlet_exit':
        menu_btn1 = InlineKeyboardButton('Close the hint',
                                         callback_data='help_outlet_back')
        keyboard_for_admins = InlineKeyboardMarkup().add(menu_btn1)

    elif data == 'help_name_month_exit':
        menu_btn1 = InlineKeyboardButton('Close the hint',
                                         callback_data='help_month_back')
        keyboard_for_admins = InlineKeyboardMarkup().add(menu_btn1)

    return keyboard_for_admins