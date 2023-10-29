from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from .checkboxes import CHECKBOXES
from lexicon.lexicon_ru import LexiconRu
from users.users import users
from utils.btn_callback_factory import BtnCallbackFactory
from utils.districts import DISTRICTS


NUM_OF_COLS = 2


def get_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=f"{CHECKBOXES[users[user_id]['btn'][idx]]} {name}",
            callback_data=BtnCallbackFactory(action='choose', idx=idx, name=name).pack(),
        )
        for idx, name in DISTRICTS.items()
    ]

    builder.row(*buttons, width=NUM_OF_COLS)

    builder.row(
        InlineKeyboardButton(
            text=LexiconRu.CONFIRM.value,
            callback_data=BtnCallbackFactory(action='finish').pack(),
        )
    )

    builder.row(
        InlineKeyboardButton(
            text=LexiconRu.RESET.value,
            callback_data=BtnCallbackFactory(action='reset').pack(),
        )
    )

    return builder.as_markup(resize_keyboard=True)


def reset_keyboard(user_id: int) -> None:
    users[user_id]['btn'] = [0] * len(DISTRICTS)
