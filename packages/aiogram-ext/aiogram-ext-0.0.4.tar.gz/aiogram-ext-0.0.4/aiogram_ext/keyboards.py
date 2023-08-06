from .buttons import InlineButton
from .deps import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
)

ReplyButton = str | KeyboardButton


class ReplyKeyboard(ReplyKeyboardMarkup):
    buttons: list[ReplyButton] = None

    def __init__(self, *buttons: str | KeyboardButton, row_width=1):
        super().__init__(row_width=row_width, resize_keyboard=True)
        self.add(*(self.buttons or []), *buttons)


class InlineKeyboard(InlineKeyboardMarkup):
    buttons: list[InlineButton] = None

    def __init__(self, *buttons: InlineButton, row_width=1):
        super().__init__(row_width=row_width)
        self.add(*(self.buttons or []), *buttons)
