from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    commands_list = [
        BotCommand(command="start", description="Getting started with the bot, menu output"),
        BotCommand(command="help", description="Information about the bot, contacts for communication"),
        BotCommand(command="cancel", description="Cancel operation"),
        BotCommand(command="get_price", description="Get dollar price"),
        BotCommand(command="set_limits", description="Set limits for tracking")
    ]
    await bot.set_my_commands(commands_list, scope=BotCommandScopeAllPrivateChats())
