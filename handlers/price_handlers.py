from aiogram import Router, types, F
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import asyncio

from logger.logger import logger

from keyboards.kb_default import default_kb
from keyboards.limits_set_kb import limits_set_kb
from keyboards.cancel_kb import cancel_kb

from utils.isfloat import isfloat
from utils.rate_price import get_price

from answer_message import *

router = Router()


class UserLimits(StatesGroup):
    """ Класс со всеми состояниями для машины состояний """
    first_limit = State()
    second_limit = State()
    limits_is_set = State()
    tracking = State()


@router.message(Command('cancel'))
@router.message(Text('Отмена'))
async def cancel_price(message: types.Message, state: FSMContext):
    """ Выход из машины состояний и из функции отслеживания, если она есть """
    data_state = await state.get_data()
    task_id = data_state.get('function_task_id')
    for task in asyncio.all_tasks():
        if task.get_name() == task_id:
            task.cancel()
    await state.clear()
    await message.answer('Операция завершена', reply_markup=default_kb())
    logger.info(f'{message.from_user.username} exited FSM or tracking function')


@router.message(Text('Получить курс $'))
@router.message(Command('get_price'))
async def get_price_handlers(message: types.Message):
    price = await get_price()
    if price is None:
        await message.answer(error_price_text, reply_markup=default_kb())
        logger.warning(f'{message.from_user.username} failed to get dollar exchange rate')
    else:
        await message.answer(get_price_text.format(price), reply_markup=default_kb())
        logger.info(f'{message.from_user.username} got the dollar rate')


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
    if data_price['second_limit'] < data_price['first_limit']:
        # Проверка больше ли нижняя граница верхней
        await message.answer(error_limits)
        await cancel_price(message, state)
    else:
        await message.answer(
            finish_set_limits_text.format(data_price['first_limit'], data_price['second_limit']),
            reply_markup=limits_set_kb())
        await state.set_state(UserLimits.limits_is_set)


# Обработка не числовых значений границ
@router.message(UserLimits.first_limit, F.text.func(lambda text: not isfloat(text)))
@router.message(UserLimits.second_limit, F.text.func(lambda text: not isfloat(text)))
async def error_input(message: types.Message):
    await message.reply(error_input_text, reply_markup=cancel_kb())


# Старт отслеживания
@router.message(UserLimits.limits_is_set, Text('Начать отслеживание цены'))
async def start_tracking(message: types.Message, state: FSMContext):
    infinite_task_tracking = asyncio.create_task(tracking_price(message, state))
    await state.update_data(function_task_id=infinite_task_tracking.get_name())
    await message.answer(start_tracking_text, reply_markup=cancel_kb())
    await state.set_state(UserLimits.tracking)
    logger.info(f'{message.from_user.username} start tracking')


# Сообщение во время отслеживания
@router.message(UserLimits.tracking)
async def is_tracking(message: types.Message):
    await message.answer(is_tracking_text, reply_markup=cancel_kb())


async def tracking_price(message: types.Message, state: FSMContext):
    data_state = await state.get_data()
    first_limit, second_limit, task_id = (value for value in data_state.values())
    while True:
        price = await get_price()
        match price:
            case price if price is None:
                logger.warning(f'{message.from_user.username} failed to get dollar exchange rate')
                await message.answer(error_price_text, reply_markup=default_kb())
                await cancel_price(message, state)

            case price if first_limit > price:
                logger.info(f'{message.from_user.username}: The dollar exchange rate is lower than the lower limit')
                await message.answer(over_first_limit_text.format(abs(first_limit - price), price),
                                     reply_markup=default_kb())
                await cancel_price(message, state)

            case price if second_limit < price:
                logger.info(f'{message.from_user.username}: The dollar is higher than the upper limit')
                await message.answer(over_second_limit_text.format(abs(second_limit - price), price),
                                     reply_markup=default_kb())
                await cancel_price(message, state)

            case _:
                await asyncio.sleep(60)
