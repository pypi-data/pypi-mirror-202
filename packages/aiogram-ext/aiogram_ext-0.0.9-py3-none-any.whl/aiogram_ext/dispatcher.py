import asyncio
from typing import TypeVar

from .buttons import CallbackButton
from .deps import Dispatcher as _Dispatcher, executor, State
from .filters import (
    CallbackQueryButton,
    InlineQueryButton,
    MessageButton,
    StorageDataFilter,
)

T = TypeVar("T")


class Dispatcher(_Dispatcher):
    @staticmethod
    def _gen_payload(
        locals_: dict, exclude: list[str] = None, default_exclude=("self", "cls")
    ):
        kwargs = locals_.pop("kwargs", {})
        locals_.update(kwargs)

        if exclude is None:
            exclude = []
        return {
            key: value
            for key, value in locals_.items()
            if key not in exclude + list(default_exclude)
            and value is not None
            and not key.startswith("_")
        }

    def _setup_filters(self):
        filters_factory = self.filters_factory
        filters_factory.bind(
            StorageDataFilter,
            exclude_event_handlers=[
                self.errors_handlers,
                self.poll_handlers,
                self.poll_answer_handlers,
            ],
        )
        filters_factory.bind(
            CallbackQueryButton, event_handlers=[self.callback_query_handlers]
        )
        filters_factory.bind(
            InlineQueryButton, event_handlers=[self.inline_query_handlers]
        )
        filters_factory.bind(
            MessageButton,
            event_handlers=[
                self.message_handlers,
                self.edited_message_handlers,
            ],
        )

        super()._setup_filters()

    def run_webhook(
        self,
        webhook_host,
        webhook_path,
        *,
        skip_updates=None,
        on_startup=None,
        on_shutdown=None,
        check_ip=False,
        retry_after=None,
        route_name=executor.DEFAULT_ROUTE_NAME,
        allowed_updates: list[str] = None,
        **kwargs,
    ):
        loop = self.loop or asyncio.get_event_loop()
        webhook_task = loop.create_task(
            self.bot.set_webhook(
                webhook_host + webhook_path,
                allowed_updates=allowed_updates,
                drop_pending_updates=skip_updates,
            )
        )
        if not loop.is_running():
            loop.run_until_complete(webhook_task)

        executor.start_webhook(
            self,
            webhook_path=webhook_path,
            loop=loop,
            skip_updates=skip_updates,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            check_ip=check_ip,
            retry_after=retry_after,
            route_name=route_name,
            **kwargs,
        )

    def message_handler(
        self,
        *custom_filters,
        text=None,
        commands=None,
        regexp=None,
        button=None,
        content_types=None,
        chat_type=None,
        state=None,
        storage=None,
        is_reply=None,
        is_forwarded=None,
        user_id=None,
        chat_id=None,
        text_startswith=None,
        text_contains=None,
        text_endswith=None,
        run_task=None,
        **kwargs,
    ):
        payload = self._gen_payload(locals(), exclude=["custom_filters"])
        return super().message_handler(*custom_filters, **payload)

    def edited_message_handler(
        self,
        *custom_filters,
        text=None,
        commands=None,
        regexp=None,
        button=None,
        content_types=None,
        chat_type=None,
        state=None,
        storage=None,
        is_reply=None,
        is_forwarded=None,
        user_id=None,
        chat_id=None,
        text_startswith=None,
        text_contains=None,
        text_endswith=None,
        run_task=None,
        **kwargs,
    ):
        payload = self._gen_payload(locals(), exclude=["custom_filters"])
        return super().edited_message_handler(*custom_filters, **payload)

    def callback_query_handler(
        self,
        *custom_filters,
        text=None,
        regexp=None,
        button=None,
        chat_type=None,
        state=None,
        storage=None,
        user_id=None,
        chat_id=None,
        text_startswith=None,
        text_contains=None,
        text_endswith=None,
        run_task=None,
        **kwargs,
    ):
        payload = self._gen_payload(locals(), exclude=["custom_filters"])
        return super().callback_query_handler(*custom_filters, **payload)

    def inline_handler(
        self,
        *custom_filters,
        text=None,
        regexp=None,
        button=None,
        state=None,
        storage=None,
        user_id=None,
        chat_id=None,
        text_startswith=None,
        text_contains=None,
        text_endswith=None,
        run_task=None,
        **kwargs,
    ):
        payload = self._gen_payload(locals(), exclude=["custom_filters"])
        return super().inline_handler(*custom_filters, **payload)

    def command(self, command: str, state: str = None):
        return self.message_handler(commands=command, state=state)

    def start(self, state: str | None = "*"):
        return self.command("start", state)

    def button(self, button: CallbackButton):
        return self.callback_query_handler(button=button)

    def text(self, text: str = None, state: str | State = None):
        return self.message_handler(button=text, state=state)

    def contact(self, state: str | State = None):
        return self.message_handler(content_types="contact", state=state)

    def document(self, state: str | State = None):
        return self.message_handler(content_types="document", state=state)

    def photo(self, state: str | State = None):
        return self.message_handler(content_types="photo", state=state)

    def run(self):
        executor.start_polling(self)
