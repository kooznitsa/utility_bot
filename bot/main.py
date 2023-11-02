import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import aioredis

from config_data.config import settings
from handlers import district_handlers
from keyboards.main_menu import set_main_menu

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.bot_token)

    redis = await aioredis.from_url(settings.redis_url, db=5)
    storage: RedisStorage = RedisStorage(redis=redis)

    dp: Dispatcher = Dispatcher(storage=storage)

    dp.include_routers(district_handlers.router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
