from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.district_keyboard import get_keyboard, reset_keyboard
from lexicon.lexicon_ru import LexiconRu
from users.users import users
from utils.btn_callback_factory import BtnCallbackFactory
from utils.districts import DISTRICTS

router = Router()


@router.message(Command(commands=['start', 'help']))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}

    reset_keyboard(message.from_user.id)

    await message.answer(
        text=LexiconRu.START.value,
        reply_markup=get_keyboard(message.from_user.id),
    )


@router.callback_query(BtnCallbackFactory.filter(F.action == 'choose'))
async def process_choose_callback(
    callback: CallbackQuery,
    callback_data: BtnCallbackFactory,
):
    btn = users[callback.from_user.id]['btn']

    if btn[callback_data.idx] == 0:
        answer = LexiconRu.ADD.value
        btn[callback_data.idx] = 1
    else:
        answer = LexiconRu.REMOVE.value
        btn[callback_data.idx] = 0

    try:
        await callback.message.edit_text(
            text=LexiconRu.ADD_MORE.value,
            reply_markup=get_keyboard(callback.from_user.id)
        )
    except TelegramBadRequest:
        pass

    await callback.answer(answer)


@router.callback_query(BtnCallbackFactory.filter(F.action == 'finish'))
async def process_finish_callback(callback: CallbackQuery):
    btns = users[callback.from_user.id]['btn']
    districts = [DISTRICTS[idx] for idx, btn in enumerate(btns) if btn == 1]

    await callback.answer(
        text=f"{LexiconRu.RESULT.value} {', '.join(districts)}",
        show_alert=True,
    )


@router.callback_query(BtnCallbackFactory.filter(F.action == 'reset'))
async def process_reset_callback(callback: CallbackQuery):
    reset_keyboard(callback.from_user.id)

    try:
        await callback.message.edit_text(
            text=LexiconRu.START.value,
            reply_markup=get_keyboard(callback.from_user.id)
        )
    except TelegramBadRequest:
        pass
