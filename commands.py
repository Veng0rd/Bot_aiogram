from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    commands_list = [
        BotCommand(command="start", description="Getting started with the bot, menu output"),
        BotCommand(command="help", description="Information about the bot, contacts for communication"),
    ]
    await bot.set_my_commands(commands_list, scope=BotCommandScopeAllPrivateChats())
