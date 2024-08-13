from typing import Any, Dict
from typing import Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import User, TelegramObject
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.managers import BaseManager

from app.infrastructure.database.db import session
from app.infrastructure.database.methods import get_user, upsert_user
from app.infrastructure.models.user import UserModel


class UserManager(BaseManager):
    async def set_locale(self, locale: str, user: UserModel) -> None:
        user.language_code = locale
        await session.commit()

    async def get_locale(self, user: UserModel) -> str:
        return user.language_code if user else "ru"


class UserMiddleware(BaseMiddleware):
    def __init__(self, i18n_middleware: I18nMiddleware):
        self.i18n_middleware = i18n_middleware

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        event_user: User = data["event_from_user"]

        user = get_user(event_user.id)
        if not user:
            user_language = event_user.language_code
            if user_language not in self.i18n_middleware.core.available_locales:
                user_language = self.i18n_middleware.core.default_locale

            upsert_user(event_user, user_language)

        data["user"] = user
        return await handler(event, data)
