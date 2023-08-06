from __future__ import annotations

from copy import deepcopy

from .deps import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    Bot,
)

DEEPLINK_BASE = "https://t.me/{bot_username}?start={start_param}"


def _get_bot_username() -> str | None:
    bot = Bot.get_current()
    try:
        return getattr(getattr(bot, "_me"), "username")
    except AttributeError:
        raise RuntimeError("Can't get bot username for deeplink")


class InlineButton(InlineKeyboardButton):
    def __init__(
        self,
        text: str,
        callback: str | bool = None,
        url: str | bool = None,
        start_param: str | bool = None,
        switch_iquery: str | bool = None,
        switch_iquery_current: str | bool = None,
    ):
        # update args
        if url is True:
            url = text
        elif start_param is True:
            start_param = text
        elif callback is True:
            callback = text
        elif switch_iquery is True:
            switch_iquery = text
        elif switch_iquery_current is True:
            switch_iquery_current = text

        # cast start_param to url
        if start_param:
            bot_username = _get_bot_username()
            url = DEEPLINK_BASE.format(
                bot_username=bot_username, start_param=start_param
            )

        super().__init__(
            text,
            url=url,
            callback_data=callback,
            switch_inline_query=switch_iquery,
            switch_inline_query_current_chat=switch_iquery_current,
        )

    def format(self, *args, **kwargs) -> InlineButton:
        """Return new button with formatted values."""
        new_button = deepcopy(self)

        for item, value in new_button.values.items():
            if isinstance(value, str):
                new_button[item] = value.format(*args, **kwargs)

        return new_button


class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, *buttons: str, row_width=1):
        super().__init__(row_width=row_width, resize_keyboard=True)
        self.add(*buttons)


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, *buttons: InlineButton, row_width=1):
        super().__init__(row_width=row_width)
        self.add(*buttons)
