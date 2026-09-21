from sqlalchemy import (String)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base



class StatusBuildBot(Base):
    __tablename__ = "status_build_bot"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    desc: Mapped[str] = mapped_column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        return f"StatusBuildBot(id={self.id}, name={self.name})"
