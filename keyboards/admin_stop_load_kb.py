from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_cancel_state = KeyboardButton('/cancel')
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_cancel_state)
