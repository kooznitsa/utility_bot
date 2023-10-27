from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .checkboxes import CHECKBOXES
from lexicon.lexicon_ru import LexiconRu
from users.users import users
from utils.btn_callback_factory import BtnCallbackFactory
from utils.districts import DISTRICTS


def get_keyboard(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for idx, name in DISTRICTS.items():
        builder.button(
            text=f"{CHECKBOXES[users[user_id]['btn'][idx]]} {name}",
            callback_data=BtnCallbackFactory(action='choose', idx=idx, name=name),
        )

    builder.button(
        text=LexiconRu.CONFIRM.value,
        callback_data=BtnCallbackFactory(action='finish'),
    )

    builder.button(
        text=LexiconRu.RESET.value,
        callback_data=BtnCallbackFactory(action='reset'),
    )

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def reset_keyboard(user_id: int) -> None:
    users[user_id]['btn'] = [0] * len(DISTRICTS)
