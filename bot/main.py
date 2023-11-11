import asyncio
import json
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import aioredis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_data.config import settings
from handlers import district_handlers
from keyboards.main_menu import set_main_menu
from receiver.driver import GatewayAPIDriver
from utils.async_iterator import AsyncItemIterator
from utils.formatter import Formatter

logging.basicConfig(level=logging.INFO)


async def get_user_ids():
    resp = await GatewayAPIDriver.tg_users_get()
    user_ids = []
    async for user in AsyncItemIterator(resp.json()):
        data = json.loads(json.dumps(user, ensure_ascii=False))
        user_ids.append(data['user_id'])
    return user_ids


async def send_articles(bot: Bot):
    user_ids = await get_user_ids()
    async for user_id in AsyncItemIterator(user_ids):
        if data := await GatewayAPIDriver.tg_articles_get(user_id):
            async for article in AsyncItemIterator(data.json()):
                text = Formatter.format_message(article)
                await bot.send_message(user_id, text)


async def main():
    bot = Bot(token=settings.bot_token, parse_mode='HTML')

    redis = await aioredis.from_url(settings.redis_url, db=5)
    storage: RedisStorage = RedisStorage(redis=redis)

    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_routers(district_handlers.router)

    await set_main_menu(bot)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_articles, 'cron', minute=5, hour='8-20',
        timezone=settings.timezone, args=(bot,),
    )
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
