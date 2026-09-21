from sqlalchemy import (
    String, 
    DateTime, 
    Integer,
    ForeignKey,
    func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.base import Base


class Bots(Base):
    __tablename__="bots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False,)
    name: Mapped[str] = mapped_column(String(100), nullable=False,)
    slug: Mapped[str] = mapped_column(String(255), nullable=True,)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_bot.id"), nullable=False,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,)

    owner: Mapped["Users"] = relationship(back_populates="bots")
    bot_versions: Mapped[list["BotVersions"]] = relationship(back_populates="bot")
    status: Mapped["StatusBot"] = relationship()

    def __repr__(self) -> str:
        return f"Bot(id={self.id}, name={self.name})"

    