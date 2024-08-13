from aiogram.filters.callback_data import CallbackData


class CompanyDataCD(CallbackData, prefix="col"):
    company_id: int
    column: str
