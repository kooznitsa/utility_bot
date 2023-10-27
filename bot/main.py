import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import settings
from handlers import district_handlers
from keyboards.main_menu import set_main_menu

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_routers(district_handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
