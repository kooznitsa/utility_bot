from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from .callback_factory import BtnCallbackFactory
from lexicon.districts import DISTRICTS
from lexicon.lexicon_ru import LexiconRu

NUM_OF_COLS = 2
CHECKBOXES = {0: '⬜', 1: '✅'}


def get_keyboard(buttons: list[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(
            text=f"{CHECKBOXES[buttons[idx]]} {name}",
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
