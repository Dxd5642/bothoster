from sqlalchemy import (
    String, 
    Boolean, 
    DateTime, 
    func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True,)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True,)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False,)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False,)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,)

    bots: Mapped[list["Bots"]] = relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"Users(id={self.id}, username={self.username}, email={self.email})"

   