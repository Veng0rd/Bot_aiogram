from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import default_handlers, price_handlers
from commands import set_commands
from logger.logger import logger


@logger.catch
async def main_bot():
    # Запуск бота
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value(), parse_mode='HTML')
    await set_commands(bot)

    # Подключение роутеров
    dp.include_router(price_handlers.router)
    dp.include_router(default_handlers.router)

    # Скип сообщений, пока был оффлайн
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
