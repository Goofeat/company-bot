from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.tgbot.callbacks.file import FileCD


def files_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for file in ["Excel", "CSV", "JSON"]:
        keyboard.button(
            text=file,
            callback_data=FileCD(file=file),
        )

    keyboard.adjust(3)

    return keyboard.as_markup()
