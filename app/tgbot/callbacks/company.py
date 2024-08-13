from aiogram.filters.callback_data import CallbackData


class CompanyCD(CallbackData, prefix="comp"):
    id: int
