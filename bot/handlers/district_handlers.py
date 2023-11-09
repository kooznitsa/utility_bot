from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.callback_factory import BtnCallbackFactory
from keyboards.district_keyboard import get_keyboard
from lexicon.districts import DISTRICTS
from lexicon.lexicon_ru import LexiconRu
from schemas.schemas import UserCreate, DistrictCreate
from receiver.driver import GatewayAPIDriver
from receiver.get_data import get_data

router = Router()


class FSMDistrict(StatesGroup):
    buttons = State()


class AsyncItemIterator:
    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            item = next(self._items)
        except StopIteration:
            raise StopAsyncIteration
        return item


async def reset_buttons(state: FSMContext) -> list[int]:
    data = await state.get_data()
    buttons = [0] * len(DISTRICTS)
    data['buttons'] = buttons
    await state.set_data(data)
    return buttons


@router.message(Command(commands='help'))
async def process_help_command(message: Message) -> None:
    await message.answer(
        text=LexiconRu.HELP_DESC.value,
    )


@router.message(Command(commands='start'))
async def process_start_command(message: Message, state: FSMContext) -> None:
    await state.set_state(FSMDistrict.buttons)

    buttons = await reset_buttons(state)

    user = UserCreate(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )

    await GatewayAPIDriver.tg_user_create(user)

    await message.answer(
        text=LexiconRu.START.value,
        reply_markup=get_keyboard(buttons),
    )


@router.callback_query(
    BtnCallbackFactory.filter(F.action == 'choose'),
    StateFilter(FSMDistrict.buttons),
)
async def process_choose_callback(
        callback: CallbackQuery,
        callback_data: BtnCallbackFactory,
        state: FSMContext,
) -> None:
    user_data = await state.get_data()
    buttons = user_data.get('buttons')

    if buttons[callback_data.idx] == 0:
        answer = LexiconRu.ADD.value
        buttons[callback_data.idx] = 1
    else:
        answer = LexiconRu.REMOVE.value
        buttons[callback_data.idx] = 0

    await state.update_data(buttons=buttons)

    try:
        await callback.message.edit_text(
            text=LexiconRu.ADD_MORE.value,
            reply_markup=get_keyboard(buttons)
        )
    except TelegramBadRequest:
        pass

    await callback.answer(answer)


@router.callback_query(BtnCallbackFactory.filter(F.action == 'reset'))
async def process_reset_callback(callback: CallbackQuery, state: FSMContext) -> None:
    buttons = await reset_buttons(state)

    try:
        await callback.message.edit_text(
            text=LexiconRu.START.value,
            reply_markup=get_keyboard(buttons)
        )
    except TelegramBadRequest:
        pass

    await state.clear()
    await callback.answer()


@router.callback_query(BtnCallbackFactory.filter(F.action == 'finish'))
async def process_finish_callback(callback: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    districts = [
        DISTRICTS[idx]
        for idx, status in enumerate(user_data['buttons']) if status == 1
    ]

    await GatewayAPIDriver.tg_districts_delete(callback.from_user.id)

    async for district in AsyncItemIterator(districts):
        await GatewayAPIDriver.tg_district_create(
            callback.from_user.id,
            DistrictCreate(district=district),
        )

    await state.clear()

    try:
        await callback.message.edit_text(
            text=f"{LexiconRu.RESULT.value} {', '.join(districts)}",
            reply_markup=None,
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


@router.message()
async def send_articles(message: Message):
    if data := get_data(message.from_user.id):
        await message.answer(text=data)
    else:
        await message.answer(text='Статьи не найдены.')
