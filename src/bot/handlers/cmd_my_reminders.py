from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import User

router = Router()

Weekdays = {
    "1": "пн",
    "2": "вт",
    "3": "ср",
    "4": "чт",
    "5": "пт",
    "6": "сб",
    "7": "вс",
    "0": "ежедневное",
    "8": "одноразовое",
}


@router.message(Command(commands=["my_reminders"]))
async def my_reminders(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    t = []
    for r in user.reminders:
        text_repeat = ", ".join([Weekdays.get(i) for i in r.repeat])
        text = f"({r.idpk}) {r.time_to_send} \[{text_repeat}] - {r.message}"
        t.append(text)
    if not t:
        t.append("У вас нет напоминаний")
    t_str = "\n".join(t)
    len_message = 4050
    if len(t_str) > len_message:
        for x in range(len(t_str)):
            x2 = x + 1
            await message.answer(text=t_str[x * len_message : x2 * len_message])
    else:
        await message.answer(text=t_str)
