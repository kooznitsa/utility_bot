from aiogram import Bot
from aiogram.types import BotCommand

from lexicon.lexicon_ru import LexiconRu


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description=LexiconRu.START.value),
    ]

    await bot.set_my_commands(main_menu_commands)
