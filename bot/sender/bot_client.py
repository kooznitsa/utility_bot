from telethon import TelegramClient

from config_data.config import settings


async def bot_init() -> TelegramClient:
    bot = TelegramClient(
        session=settings.tg_session_name,
        api_id=settings.tg_api_id,
        api_hash=settings.tg_api_hash,
    )

    return await bot.start(bot_token=settings.tg_bot_token)
