from sqlalchemy import\
    Text,\
    DateTime
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column
from .base import\
    Base
from datetime import\
    datetime


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    lastname: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_valid_token: Mapped[Optional[str]] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r}, email={self.email!r})"

