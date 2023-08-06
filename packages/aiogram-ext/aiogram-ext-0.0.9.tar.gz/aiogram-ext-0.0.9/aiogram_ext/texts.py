import toml


class Texts:
    def __init__(self, path: str) -> None:
        self._items = toml.load(path)

    def get_words(self, key: int) -> list[str]:
        text = self[key]
        return text.lower().split()

    def __getitem__(self, item: int) -> str:
        key = str(item)
        if key in self._items:
            return str(self._items[key])
        raise TextsKeyError(key)


class TextsKeyError(KeyError):
    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self) -> str:
        return f"No text with key `{self.key}`"
