from enum import Enum, unique


@unique
class LexiconRu(Enum):
    START = 'Выберите район(-ы):'
    ADD = 'Добавлено!'
    REMOVE = 'Удалено!'
    ADD_MORE = 'Вы можете добавить больше районов'
    CONFIRM = '☑️ Подтвердить'
    RESET = '🔄 Сброс'
    RESULT = 'Вы подписались на уведомления по району(-ам):'
