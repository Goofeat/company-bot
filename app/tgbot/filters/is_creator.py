from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.infrastructure.database.db import config


class IsCreator(BaseFilter):
    def __init__(self) -> None:
        self.admin_id = config.bot.admin_id

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.admin_id
