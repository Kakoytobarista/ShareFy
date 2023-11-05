import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String, DateTime, Enum

from app.enums import PersonTypeEnum

Base = declarative_base()


class AuthUserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    date_of_birth: Mapped[DateTime] = mapped_column(DateTime)
    person_type: Mapped[Enum] = mapped_column(Enum(PersonTypeEnum.REGULAR.value,
                                                   PersonTypeEnum.MODERATOR.value,
                                                   PersonTypeEnum.ADMIN.value), default='regular')
    date_of_create: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now())
