from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.infrastructure.database.methods import fetch_companies
from app.tgbot.callbacks.company import CompanyCD


def companies_kb() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    companies = fetch_companies()

    for company in companies:
        keyboard.button(
            text=f"{company.id}. {company.name}",
            callback_data=CompanyCD(id=company.id),
        )

    keyboard.adjust(1)

    return keyboard.as_markup()
