from aiogram import Router, types
from aiogram.filters import Command

from keyboards.kb_default import default_kb
from answer_message import info_text, help_text

router = Router()


@router.message(Command('start'))
async def start_handlers(message: types.Message):
    await message.answer('Привет <b>{first_name}</b>!\n{text}'.format(first_name=message.from_user.first_name,
                                                                      text=info_text), reply_markup=default_kb())


@router.message(Command('help'))
async def help_handlers(message: types.Message):
    await message.answer(info_text)
    await message.answer(help_text, reply_markup=default_kb())
