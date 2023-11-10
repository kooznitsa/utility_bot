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
