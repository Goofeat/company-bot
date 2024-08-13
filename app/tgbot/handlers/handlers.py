import io
from typing import Any

import matplotlib.pyplot as plt
from aiogram import Router, F, Bot
from aiogram.filters import (
    Command,
    CommandStart, StateFilter,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, BufferedInputFile, ReplyKeyboardMarkup, KeyboardButton, FSInputFile, )
from aiogram_i18n import I18nContext

from app.infrastructure.database.methods import get_revenue, get_expenses, get_profit, get_tax, get_name, \
    get_revenue_list, get_expenses_list, get_profit_list, get_tax_list, parse_data
from app.tgbot.callbacks.company import CompanyCD
from app.tgbot.callbacks.company_data import CompanyDataCD
from app.tgbot.callbacks.file import FileCD
from app.tgbot.keyboards.companies import companies_kb
from app.tgbot.keyboards.company_data import company_data_kb
from app.tgbot.keyboards.files import files_kb
from app.tgbot.states.file import FileSG

router = Router()


@router.message(F.document, StateFilter(FileSG.wait_for_file))
async def document_handler(message: Message, bot: Bot, i18n: I18nContext, state: FSMContext):
    file_name = message.document.file_name

    file_format = file_name[file_name.rfind('.') + 1:]

    if file_format not in ["xlsx", "csv", "json"]:
        return await message.answer(i18n.upload.error())

    file_path = f"uploads/{file_format}/{message.document.file_id}.{file_format}"

    await bot.download(
        file=message.document,
        destination=file_path,
    )

    parse_data(file_path)
    await state.clear()

    await message.answer(i18n.upload.success())


@router.callback_query(FileCD.filter())
async def file_query(callback: CallbackQuery, callback_data: FileCD, i18n: I18nContext, state: FSMContext) -> Any:
    await callback.answer()

    caption = getattr(i18n.example, callback_data.file.lower())
    file_format = callback_data.file.lower()
    if file_format == "excel":
        file_format = "xlsx"

    await state.set_state(FileSG.wait_for_file)

    await callback.message.delete()

    await callback.message.answer_document(
        document=FSInputFile(f"examples/example.{file_format}"),
        caption=caption()
    )
    await callback.message.answer(
        i18n.upload.file()
    )


@router.message(Command("upload"))
@router.message(F.text.lower() == "⬆️ загрузить данные")
async def file_handler(message: Message, i18n: I18nContext) -> Any:
    await message.answer(
        text=i18n.upload.cmd(),
        reply_markup=files_kb()
    )


@router.callback_query(CompanyCD.filter())
async def company_query(callback: CallbackQuery, callback_data: CompanyCD, i18n: I18nContext) -> Any:
    await callback.answer()

    company_name = get_name(company_id=callback_data.id)
    total_revenue = get_revenue(company_id=callback_data.id)
    total_expenses = get_expenses(company_id=callback_data.id)
    total_profit = get_profit(company_id=callback_data.id)
    total_tax = get_tax(company_id=callback_data.id)

    await callback.message.edit_text(
        text=i18n.company.cmd(
            name=company_name,
            revenue=total_revenue,
            expenses=total_expenses,
            profit=total_profit,
            tax=total_tax,
        ),
        reply_markup=company_data_kb(callback_data.id, i18n)
    )


@router.callback_query(CompanyDataCD.filter())
async def company_data_query(callback: CallbackQuery, callback_data: CompanyDataCD, i18n: I18nContext) -> Any:
    await callback.answer()

    # months = ['January', 'February', 'March', 'April',
    #           'May', 'June', 'July', 'August',
    #           'September', 'October', 'November', 'December']
    months = ['Январь', 'Февраль', 'Март', 'Апрель',
              'Май', 'Июнь', 'Июль', 'Август',
              'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    plt.figure(figsize=(12, 6))

    if callback_data.column == "revenue":
        revenue = get_revenue_list(company_id=callback_data.company_id)
        plt.bar(months, revenue, label=i18n.revenue(), color='blue')
    elif callback_data.column == "expenses":
        expenses = get_expenses_list(company_id=callback_data.company_id)
        plt.bar(months, expenses, label=i18n.expenses(), color='red')
    elif callback_data.column == "profit":
        profit = get_profit_list(company_id=callback_data.company_id)
        plt.bar(months, profit, label=i18n.profit(), color='green')
    elif callback_data.column == "tax":
        tax = get_tax_list(company_id=callback_data.company_id)
        plt.bar(months, tax, label=i18n.tax(), color='gray')
    elif callback_data.column == "back":
        return await callback.message.edit_text(
            text=i18n.companies.cmd(),
            reply_markup=companies_kb(),
        )

    plt.xlabel("Месяц")
    plt.ylabel('Сумма в ₸')
    plt.yticks([number * 1_000_000 for number in range(11)])
    plt.title('Финансовые данные компании')
    plt.legend()
    plt.xticks(rotation=30)
    plt.grid(True, axis="y", linestyle='dashed')

    plt.ticklabel_format(style='plain', axis='y')

    buffer = io.BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await callback.message.answer_photo(
        photo=BufferedInputFile(
            buffer.read(), "plot.png"
        ),
        caption=i18n.plot(name=get_name(callback_data.company_id)),
    )


@router.message(Command("companies"))
@router.message(F.text.lower() == "💼 компании")
async def companies_handler(message: Message, i18n: I18nContext) -> Any:
    await message.answer(
        text=i18n.companies.cmd(),
        reply_markup=companies_kb(),
    )


@router.message(CommandStart())
async def start_handler(message: Message, i18n: I18nContext) -> Any:
    await message.answer(
        text=i18n.start.cmd(),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=i18n.companies()),
                    KeyboardButton(text=i18n.upload()),
                ],
                [
                    KeyboardButton(text=i18n.help())
                ]
            ],
            resize_keyboard=True,
        ),
    )


@router.callback_query(F.data == "help")
async def help_query(callback: CallbackQuery, i18n: I18nContext) -> Any:
    await callback.answer()
    await callback.message.answer(text=i18n.help.cmd())


@router.message(F.text.lower() == "❓ помощь")
@router.message(Command("help"))
async def help_handler(message: Message, i18n: I18nContext) -> Any:
    await message.answer(text=i18n.help.cmd())
