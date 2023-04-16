from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text='Отмена')
    )
    return keyboard.as_markup(resize_keyboard=True)
