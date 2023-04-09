from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def default_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text='Получить курс $'),
        KeyboardButton(text='Задать границы')
    )
    return keyboard.as_markup(resize_keyboard=True)


def cancel_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text='Отмена')
    )
    return keyboard.as_markup(resize_keyboard=True)


def limits_set_kb():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(
        KeyboardButton(text='Начать отслеживание цены'),
        KeyboardButton(text='Отмена')
    )
    return keyboard.as_markup(resize_keyboard=True)
