import datetime
from aiogram import F, Router
from aiogram.filters import CommandObject, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.states import UserState
from tools import parse_tasks

from db import User, Reminder

router = Router()


@router.message(F.text.startswith("удалить"))
async def del_remind(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    try:
        tasks_id = message.text.split(maxsplit=1)[1].split(",")
    except Exception:
        return await message.answer(text="Слишком много аргументов")
    try:
        tasks_id = [int(i.strip()) for i in tasks_id]
    except Exception:
        return await message.answer(text="Неверный формат id")
    for task_id in tasks_id:
        r = await session.get(Reminder, task_id)
        if not r:
            await message.answer(text=f"Напоминание с id {task_id} не найдена")
        else:
            await session.delete(r)
    await session.commit()
    await message.answer(text="напоминания удалены")
