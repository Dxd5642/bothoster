from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select, MetaData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):

    metadata = MetaData(naming_convention=convention)

    @classmethod
    async def get(
        cls,
        session: AsyncSession,
        **filters: Any
    ):
        """
        Получение данных из моделей
        """
        query = select(cls).filter_by(**filters)

        result = await session.execute(query)

        return result.scalar_one_or_none()



    @classmethod
    async def put(
        cls,
        session: AsyncSession,
        **data: Any
    ):
        """
        Создание записи для любой модели.
        """

        obj = cls(**data)

        if hasattr(obj, "updated_at"):
            obj.updated_at = datetime.now(timezone.utc)

        session.add(obj)

        await session.commit()
        await session.refresh(obj)

        return obj

    @classmethod
    async def patch(
        cls,
        session: AsyncSession,
        obj_id: Any,
        **fields: Any
    ) -> bool:
        """
        Обновление только переданных полей.
        """

        pk_columns = cls.__mapper__.primary_key

        if len(pk_columns) != 1:
            raise ValueError(
                f"{cls.__name__} must have a single primary key"
            )

        pk = pk_columns[0]

        obj = await session.get(cls, obj_id)

        if obj is None:
            return False

        protected_fields = {
            pk.key,
            "created_at",
        }

        allowed_fields = {
            column.key
            for column in cls.__table__.columns
        } - protected_fields

        invalid_fields = fields.keys() - allowed_fields

        if invalid_fields:
            raise ValueError(
                f"Invalid fields: {', '.join(invalid_fields)}"
            )

        if not fields:
            return False

        for key, value in fields.items():
            setattr(obj, key, value)

        if hasattr(obj, "updated_at"):
            obj.updated_at = datetime.now(timezone.utc)

        await session.commit()
        await session.refresh(obj)

        return True

    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        obj_id: Any
    ) -> bool:
        """
        Удаление записи по первичному ключу.
        """

        obj = await session.get(cls, obj_id)

        if obj is None:
            return False

        await session.delete(obj)
        await session.commit()

        return True