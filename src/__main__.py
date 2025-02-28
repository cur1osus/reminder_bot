import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.handlers import setup_message_routers
from bot.middlewares import (
    CheckUser,
    DBSessionMiddleware,
    ThrottlingMiddleware,
)
from config import config
from db import Base
from init_bot import bot
from init_db import _engine, _sessionmaker
from init_db_redis import redis
import aioschedule
from tasks import set_tasks_func


async def on_startup(_engine: AsyncEngine) -> None:
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        name_bot = await bot.get_my_name()
        print(f"Name Bot: {name_bot.name}")
        print(f"ID Bot: {bot.id}")


async def on_shutdown(session: AsyncSession) -> None:
    await session.close_all()


async def scheduler() -> None:
    aioschedule.every(5).seconds.do(set_tasks_func, schedule=aioschedule)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(
                command="start",
                description="start",
            ),
            BotCommand(
                command="add_task",
                description="Добавить напоминания",
            ),
            BotCommand(
                command="my_reminders",
                description="Мои напоминания",
            ),
        ]
    )


async def main() -> None:
    dp = Dispatcher(_engine=_engine, storage=RedisStorage(redis=redis))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.message.middleware(ThrottlingMiddleware())

    dp.message.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.callback_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.inline_query.middleware(DBSessionMiddleware(session_pool=_sessionmaker))
    dp.update.middleware(DBSessionMiddleware(session_pool=_sessionmaker))

    dp.message.middleware(CheckUser())
    dp.callback_query.middleware(CheckUser())
    dp.inline_query.middleware(CheckUser())

    message_routers = setup_message_routers()
    asyncio.create_task(scheduler())
    dp.include_router(message_routers)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
