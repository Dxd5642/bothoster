from sqlalchemy import (
    ForeignKey,  
    Integer
)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

class UserRoles(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False,)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), primary_key=True, nullable=False,)