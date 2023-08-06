from typing import Awaitable

from .deps import ReplyKeyboardRemove, Message, Query
from .keyboards import ReplyKeyboard, InlineKeyboard


def reply(
    msg: Message | Query,
    text: str,
    markup: ReplyKeyboard | InlineKeyboard | bool = None,
) -> Awaitable[Message]:
    if isinstance(msg, Query):
        msg = msg.message
    if markup is False:
        markup = ReplyKeyboardRemove()
    return msg.answer(text, reply_markup=markup)
