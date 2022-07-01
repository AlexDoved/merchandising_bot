from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def keyboard_for_users(data):
    """Создание инлайн-клавиатуры для пользователей."""
    global keyboard_for_users
    if data == 'start_keyboard':
        menu_btn1 = InlineKeyboardButton('📁 Get a document',
                                         callback_data='samples_doc')
        menu_btn2 = InlineKeyboardButton('🌠 Get a photo',
                                         callback_data='outlets_img')
        keyboard_for_users = InlineKeyboardMarkup().add(menu_btn1).add(
            menu_btn2)

    elif data == 'samples_open':
        doc_btn1 = InlineKeyboardButton('👞 Brand 1',
                                        callback_data='doc_brand_1')
        doc_btn2 = InlineKeyboardButton('👗 Brand 2',
                                        callback_data='doc_brand_2')
        doc_exit = InlineKeyboardButton('Back', callback_data='samples_back')
        keyboard_for_users = InlineKeyboardMarkup().add(
            doc_btn1, doc_btn2).add(
            doc_exit)

    elif data == 'outlets_open':
        brand_btn1 = InlineKeyboardButton('👞 Brand 1',
                                          callback_data='fb_img')
        brand_btn2 = InlineKeyboardButton('👗 Brand 2',
                                          callback_data='sb_img')
        brand_exit = InlineKeyboardButton('Back',
                                          callback_data='outlets_back')
        keyboard_for_users = InlineKeyboardMarkup().add(
            brand_btn1, brand_btn2).add(
            brand_exit)

    elif data == 'first_brand_open':
        fb_btn1 = InlineKeyboardButton('🔝 Moscow',
                                        callback_data='fb_moscow')
        fb_btn2 = InlineKeyboardButton('💰 Omsk',
                                        callback_data='fb_omsk')
        fb_exit = InlineKeyboardButton('Back', callback_data='fb_back')
        keyboard_for_users = InlineKeyboardMarkup().add(
            fb_btn1, fb_btn2).add(
            fb_exit)


    elif data == 'second_brand_open':
        sb_btn1 = InlineKeyboardButton('💰 Samara',
                                        callback_data='sb_samara')
        sb_btn2 = InlineKeyboardButton('🔝 Dagestan',
                                        callback_data='sb_dagestan')
        sb_exit = InlineKeyboardButton('Back', callback_data='fb_back')
        keyboard_for_users = InlineKeyboardMarkup().add(
            sb_btn1, sb_btn2).add(
            sb_exit)

    return keyboard_for_users
