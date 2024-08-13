import logging
from collections.abc import Callable, Awaitable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        user_fullname = event.from_user.full_name
        user_username = event.from_user.username
        message_text = event.text
        chat_name = event.chat.full_name
        logging.info(
            f"User ID: {user_id}, User: {user_fullname} (@{user_username}), "
            f"Message: {message_text}, Chat: {chat_name}"
        )
        return await handler(event, data)
