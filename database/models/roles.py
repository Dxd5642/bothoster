from sqlalchemy import (
    String, 
    Text,
    Boolean, 
    DateTime, 

    func)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database.base import Base

class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    name: Mapped[str] = mapped_column(String(25), default="user", nullable=False,)
    desc: Mapped[str] = mapped_column(String(255), nullable="True",)

    def __repr__(self):
        return f"Roles(id={self.id}, name={self.name})"