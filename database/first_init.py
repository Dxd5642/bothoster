from database.models.status_bot import StatusBot
from database.models.status_build_bot import StatusBuildBot
from database.models.roles import Roles
from database.connection import async_session_maker

from pathlib import Path

async def fill_status_bot_model(session):
    data = {
        "draft": "Бот создан, но ещё не запущен",
        "active": "Бот работает",
        "paused": "Бот приостановлен",
        "error": "Произошла ошибка",
        "archived": "Бот архивирован",
        }

    for name, desc in data.items():
        await StatusBuildBot.put(session, name=name, desc=desc)

async def fill_status_build_bot(session):
    data = {
        "draft": "Версия подготовлена",
        "building": "Выполняется сборка",
        "ready": "Сборка успешно завершена",
        "failed": "Сборка завершилась ошибкой",
        }

    for name, desc in data.items():
        await Roles.put(session, name=name, desc=desc)

async def fill_roles(session):
    data = {
        "roles": "Обычный пользователь",
        "admin": "Администратор",
        }

    for name, desc in data.items():
        await StatusBot.put(session, name=name, desc=desc)

async def first_init():
    """
    Функция для первой инициализации БД
    """
    
    async with async_session_maker() as session:
        status =  await StatusBot.get(session, id=1)

        if status is None:
            await fill_status_bot_model(session)
            await fill_status_build_bot(session)
            await fill_roles(session)

            return True

        return False

