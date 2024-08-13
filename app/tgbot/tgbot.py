import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import SimpleEventIsolation, MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from app.infrastructure.database.db import config
from app.tgbot.handlers import router
from app.tgbot.middlewares.logging import LoggingMiddleware
from app.tgbot.middlewares.translations import UserManager, UserMiddleware


async def main() -> None:
    logging.info("Starting bot")
    storage = MemoryStorage()
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    dp = Dispatcher(
        storage=storage,
        events_isolation=SimpleEventIsolation(),
    )

    connect_routers(dp)

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(path="locales/{locale}"),
        default_locale="ru",
        manager=UserManager(),
    )

    connect_middlewares(dp, i18n_middleware)

    i18n_middleware.setup(dispatcher=dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


def connect_routers(dp: Dispatcher) -> None:
    logging.info("Including routers")
    dp.include_router(router)


def connect_middlewares(dp, i18n_middleware):
    logging.info("Including middlewares")
    dp.update.outer_middleware(UserMiddleware(i18n_middleware))
    dp.message.middleware(LoggingMiddleware())
