from aiogram.filters.callback_data import CallbackData


class FileCD(CallbackData, prefix="file"):
    file: str
