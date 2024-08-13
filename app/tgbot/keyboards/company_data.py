from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from app.tgbot.callbacks.company_data import CompanyDataCD


def company_data_kb(company_id: int, i18n: I18nContext) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for column in ["revenue", "expenses", "profit", "tax", "back"]:
        keyboard.button(
            text=i18n.get(column),
            callback_data=CompanyDataCD(company_id=company_id, column=column),
        )

    keyboard.adjust(2)

    return keyboard.as_markup()
