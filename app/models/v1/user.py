import datetime
import enum

from enums import PersonTypeEnum
from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    person_type: Mapped[enum.Enum] = mapped_column(Enum(PersonTypeEnum), default=PersonTypeEnum.REGULAR)
    date_of_create: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now())
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True, nullable=False)
