from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import default_commands, price_handlers
from commands import set_commands


async def main_bot():
    # Запуск бота
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
    # await set_commands(bot)
    # Подключение роутеров
    dp.include_router(price_handlers.router)
    dp.include_router(default_commands.router)

    # Скип сообщений, пока был оффлайн
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
