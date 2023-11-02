from aiogram.filters.callback_data import CallbackData


class BtnCallbackFactory(CallbackData, prefix='user_btn'):
    action: str
    idx: int | None = None
    name: str | None = None
