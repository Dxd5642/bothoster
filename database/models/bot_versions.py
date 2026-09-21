from sqlalchemy import (
    String, 
    Text,
    DateTime, 
    Integer,
    ForeignKey,
    JSON,
    func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database.base import Base


class BotVersions(Base):
    __tablename__ = "bot_versions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    bot_id: Mapped[int] = mapped_column(Integer, ForeignKey("bots.id"), nullable=False,)
    version: Mapped[int] = mapped_column(Integer, nullable=False,)
    artifact_url: Mapped[str] = mapped_column(Text, nullable=True,)
    entrypoint: Mapped[str] = mapped_column(String(100), nullable=False,)
    runtime: Mapped[str] = mapped_column(String(100), nullable=False,)
    runtime_version: Mapped[str] = mapped_column(String(10), nullable=False,)
    config: Mapped[dict] = mapped_column(JSON, nullable=True,)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_build_bot.id"), nullable=False,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)

    bot: Mapped["Bots"] = relationship(back_populates="bot_versions")
    status: Mapped["StatusBuildBot"] = relationship()

    def __repr__(self) -> str:
        return f"BotVersions(id={self.id})"

   