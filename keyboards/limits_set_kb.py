from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def limits_set_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text='Начать отслеживание цены'),
        KeyboardButton(text='Отмена')
    )
    return keyboard.as_markup(resize_keyboard=True)
