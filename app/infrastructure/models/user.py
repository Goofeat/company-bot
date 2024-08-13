from sqlalchemy import Column, Integer, String

from app.infrastructure.models.base import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    fullname = Column(String, nullable=False)
    mention_html = Column(String)
    language_code = Column(String(2))
