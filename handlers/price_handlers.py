import asyncio

from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.kb_default import default_kb, cancel_kb, limits_set_kb
from rate_price import get_price
from answer_message import *

router = Router()
is_running = True


class UserLimits(StatesGroup):
    first_limit = State()
    second_limit = State()
    tracking = State()


def isfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    return True


"""Выход из машины состояний по команде /cancel или тексту 'Отмена'"""


@router.message(UserLimits.first_limit, Command('cancel'))
@router.message(UserLimits.second_limit, Command('cancel'))
@router.message(UserLimits.tracking, Command('cancel'))
@router.message(UserLimits.first_limit, Text('Отмена'))
@router.message(UserLimits.second_limit, Text('Отмена'))
@router.message(UserLimits.tracking, Text('Отмена'))
async def cancel_price(message: types.Message, state: FSMContext):
    await message.answer('Остановил работу', reply_markup=default_kb())
    data_state = await state.get_data()
    task_id = data_state.get('function_task_id')
    for task in asyncio.all_tasks():
        if task.get_name() == task_id:
            task.cancel()
    await state.clear()


@router.message(Text('Получить курс $'))
@router.message(Command('get_price'))
async def get_price_handlers(message: types.Message):
    price = await get_price()
    await message.answer(f'Курс доллара на данную минуту составляет: <b>{price}</b> руб', reply_markup=default_kb())


'''Запускается машина состояний для задания границ'''


@router.message(Text('Задать границы'))
@router.message(Command('set_limits'))
async def set_limits(message: types.Message, state: FSMContext):
    await message.answer(first_limit_text, reply_markup=cancel_kb())
    await state.set_state(UserLimits.first_limit)


# Обработка первой границы
@router.message(UserLimits.first_limit, F.text.func(lambda text: isfloat(text)))
async def set_first_limit(message: types.Message, state: FSMContext):
    await state.update_data(first_limit=float(message.text))
    await message.answer(second_limit_text, reply_markup=cancel_kb())
    await state.set_state(UserLimits.second_limit)


# Обработка второй границы
@router.message(UserLimits.second_limit, F.text.func(lambda text: isfloat(text)))
async def set_second_limit(message: types.Message, state: FSMContext):
    await state.update_data(second_limit=float(message.text))
    data_price = await state.get_data()
    await message.answer(
        finish_set_limits_text.format(first=data_price['first_limit'], second=data_price['second_limit']),
        reply_markup=limits_set_kb())
    await state.set_state(UserLimits.tracking)


# Обработка не числовых значений границ
@router.message(UserLimits.first_limit, F.text.func(lambda text: not isfloat(text)))
@router.message(UserLimits.second_limit, F.text.func(lambda text: not isfloat(text)))
async def error_input(message: types.Message):
    await message.reply(error_input_text, reply_markup=cancel_kb())


@router.message(UserLimits.tracking, Text('Начать отслеживание цены'))
async def start_tracking(message: types.Message, state: FSMContext):
    infinite_task_tracking = asyncio.ensure_future(tracking_price(message, state))
    await state.update_data(function_task_id=infinite_task_tracking.get_name())
    await message.answer('Начал работу')



async def tracking_price(message: types.Message, state: FSMContext):
    data_state = await state.get_data()
    first_limit, second_limit, task_id = (value for value in data_state.values())
    while True:
        price = await get_price()
        await message.answer('Проверка цены')
        if first_limit > float(price):
            await message.answer(f'Цена вышла за нижнюю границу!\n'
                                 f'Составляет {price}')
            await state.clear()
            for task in asyncio.all_tasks():
                if task.get_name() == task_id:
                    task.cancel()
        elif second_limit < float(price):
            await message.answer('Цена вышла за верхнюю границу!\n'
                                 f'Составляет {price}')
            await state.clear()

            for task in asyncio.all_tasks():
                if task.get_name() == task_id:
                    task.cancel()
        await asyncio.sleep(60)


@router.message(UserLimits.tracking)
async def is_tracking(message: types.Message):
    await message.answer('Я работаю')
