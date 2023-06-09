from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def default_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text='Получить курс $'),
        KeyboardButton(text='Задать границы')
    )
    return keyboard.as_markup(resize_keyboard=True)
