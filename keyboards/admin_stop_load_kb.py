from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_cancel_state_sample = KeyboardButton('/cancel-pdf')
button_cancel_state_point = KeyboardButton('/cancel-outlet')
kb_cancel_sample = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_cancel_state_sample)
kb_cancel_outlet = ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_cancel_state_point)
