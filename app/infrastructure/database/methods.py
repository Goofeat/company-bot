import csv
import json
from typing import Literal, List

import pandas as pd
from aiogram.types import User
from sqlalchemy import func

from app.infrastructure.database.db import session
from app.infrastructure.models.company import Company, CompanyData
from app.infrastructure.models.user import UserModel


# === User-related functions ===

def upsert_user(user: User, language_code: str) -> None:
    user_data = {
        "id": user.id,
        "username": user.username,
        "fullname": user.full_name,
        "mention_html": user.mention_html(),
        "language_code": language_code,
    }
    session.merge(UserModel(**user_data))
    session.commit()


def get_user(user_id: int) -> UserModel:
    return session.query(UserModel).filter_by(id=user_id).first()


# === Company-related functions ===

def fetch_companies() -> List[Company]:
    return session.query(Company).all()


def get_name(company_id: int) -> str:
    return session.query(Company.name).filter_by(id=company_id).scalar()


# === Financial data functions ===

Month = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Column = Literal["revenue", "expenses", "profit", "tax"]


def get_financial_data(
        company_id: int,
        metric: Column,
        start: Month = 1,
        end: Month = 12
) -> int:
    metric_column = getattr(CompanyData, metric)
    result = session.query(
        func.sum(metric_column)
    ).filter(
        CompanyData.company_id == company_id,
        CompanyData.month.between(start, end)
    ).scalar()
    return result or 0


def get_revenue(company_id: int, start: Month = 1, end: Month = 12) -> int:
    return get_financial_data(company_id, 'revenue', start, end)


def get_expenses(company_id: int, start: Month = 1, end: Month = 12) -> int:
    return get_financial_data(company_id, 'expenses', start, end)


def get_profit(company_id: int, start: Month = 1, end: Month = 12) -> int:
    return get_financial_data(company_id, 'profit', start, end)


def get_tax(company_id: int, start: Month = 1, end: Month = 12) -> int:
    return get_financial_data(company_id, 'tax', start, end)


def get_list(company_id: int, metric: Column) -> List[int]:
    metric_column = getattr(CompanyData, metric)
    results = session.query(metric_column).filter_by(company_id=company_id).order_by(CompanyData.month).all()
    return [result[0] for result in results]


def get_revenue_list(company_id: int) -> List[int]:
    return get_list(company_id, "revenue")


def get_expenses_list(company_id: int) -> List[int]:
    return get_list(company_id, "expenses")


def get_profit_list(company_id: int) -> List[int]:
    return get_list(company_id, "profit")


def get_tax_list(company_id: int) -> List[int]:
    return get_list(company_id, "tax")


# === Data parsing functions ===

def parse_data(file_path: str) -> None:
    if "xlsx" in file_path:
        parse_excel(file_path)
    elif "csv" in file_path:
        parse_csv(file_path)
    elif "json" in file_path:
        parse_json(file_path)


def process_company_data(data) -> None:
    company_name = data['company_name']
    company = session.query(Company).filter_by(name=company_name).first()

    if company is None:
        company = Company(name=company_name)
        session.add(company)
        session.commit()

    company_data = CompanyData(
        company_id=company.id,
        month=int(data['month']),
        revenue=int(data['revenue']),
        expenses=int(data['expenses']),
        profit=int(data['profit']),
        tax=int(data['tax'])
    )
    session.add(company_data)


def parse_excel(file_path: str) -> None:
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        process_company_data(row)
    session.commit()


def parse_csv(file_path: str) -> None:
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            process_company_data(row)
    session.commit()


def parse_json(file_path: str) -> None:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for row in data:
            process_company_data(row)
    session.commit()
