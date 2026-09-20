from sqlalchemy import String, Text, DateTime, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True,)
    username: Mapped[str] = mapped_column(String(100), nullable=False,)
    email: Mapped[str] = mapped_column(String(100), nullable=False,)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)

    def __repr__(self) -> str:
        return f"Users(id={self.id}, username={self.username})"

    @classmethod
    async def get(cls, session: AsyncSession, **filters) -> "Users | None":
        query = select(cls).filter_by(**filters)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def put(cls, session: AsyncSession, username: str, email: str, password_hash: str):
        user = cls(
            username=username,
            email=email,
            password_hash=password_hash
        )
        session.add(user)
        await session.commit()
        print(3)
        await session.refresh(user)

        return True