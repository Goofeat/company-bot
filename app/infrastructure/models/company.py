from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.models.base import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    company_datas = relationship("CompanyData", back_populates="company")


class CompanyData(Base):
    __tablename__ = "company_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    year = Column(Integer)
    month = Column(Integer)
    revenue = Column(Integer)
    expenses = Column(Integer)
    profit = Column(Integer)
    tax = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    company = relationship("Company", back_populates="company_datas")
