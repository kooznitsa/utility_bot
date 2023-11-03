import asyncio

from .bot_client import bot_init

# TODO: parse URL '/api/articles?district={d1}&district={d2}...'
# TODO: send parsed JSON to user as a message
# TODO: possible solution: Webhook


async def message_send(message) -> None:
    async with await bot_init() as bot:
        await bot.send_message(message.chat_id, message.text)


async def message_send_multiple(messages: list) -> None:
    async with bot_init() as bot:
        await asyncio.gather(*[bot.send_message(msg.chat_id, msg.text) for msg in messages])
