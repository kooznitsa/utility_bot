from collections.abc import AsyncIterable


class AsyncItems(AsyncIterable):
    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self
