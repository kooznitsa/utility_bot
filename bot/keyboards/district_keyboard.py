from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from users.users import users
from utils.btn_callback_factory import BtnCallbackFactory
from utils.checkboxes import CHECKBOXES
from utils.commands import Commands
from utils.districts import DISTRICTS


def get_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for idx, name in zip(range(len(DISTRICTS)), DISTRICTS):
        builder.button(
            text=f"{CHECKBOXES[users[user_id]['btn'][idx]]} {name}",
            callback_data=BtnCallbackFactory(action='choose', idx=idx, name=name),
        )

    builder.button(
        text=Commands.CONFIRM.value,
        callback_data=BtnCallbackFactory(action='finish'),
    )

    builder.button(
        text=Commands.RESET.value,
        callback_data=BtnCallbackFactory(action='reset'),
    )

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def reset_keyboard(user_id: int) -> None:
    users[user_id]['btn'] = [0] * len(DISTRICTS)
