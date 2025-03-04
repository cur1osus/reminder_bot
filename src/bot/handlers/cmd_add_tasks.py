from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import UserState
from db import Reminder, User
from tools import parse_tasks

router = Router()


@router.message(Command(commands=["add_task"]))
async def add_tasks(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    await message.answer(
        text="""
Отправьте напоминания списком
Формат:
[время] [повторение] [сообщение]

Повторения указываются в виде комбинации или просто цифры, где 1 - понедельник, и так далее до 7 - воскресенье. Особые повторения, 0 - ежедневное и 8 - одноразовое.

Например:
8:30 456 С добрым утром!
9:40 0 Выгулять собаку
"""
    )
    await state.set_state(UserState.add_tasks)


@router.message(UserState.add_tasks)
async def get_tasks(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    tasks = parse_tasks(message.text)
    if not tasks:
        return await message.answer(text="Напоминания не распознаны")
    for time, msg, repeat in tasks:
        try:
            int(repeat)
        except Exception:
            return await message.answer(
                text=f"Данное '{repeat}' повторение напоминания не удалось распознать, отправьте напоминания повторно с исправлением"
            )
        if not msg:
            return await message.answer(
                text=f"Сообщение на {time} для напоминания пусто"
            )
        r = Reminder(
            user=user,
            message=msg,
            repeat=repeat,
            time_to_send=time,
        )
        session.add(r)
    await session.commit()
    await state.clear()
    await message.answer(text="Напоминания добавлены")
