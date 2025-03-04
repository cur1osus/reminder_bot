from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import Reminder, User

router = Router()


@router.message(F.text.startswith("удалить"))
async def del_remind(
    message: Message,
    session: AsyncSession,
    schedule,
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
            schedule.clear(tag=task_id)
            await session.delete(r)
    await session.commit()
    await message.answer(text="Напоминания удалены")
