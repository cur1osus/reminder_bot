from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from db import Reminder, User

router = Router()

@router.message(F.text.startswith("удалить все"))
async def del_all_reminds(
    message: Message,
    session: AsyncSession,
    schedule,
    user: User,
):
    stmn = delete(Reminder).where(Reminder.idpk_user == user.idpk)
    await session.execute(stmn)
    await session.commit()
    schedule.clear(user.idpk)
    await message.answer(text="Напоминания удалены")

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
        return await message.answer(text="Ошибка аргументов")
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



