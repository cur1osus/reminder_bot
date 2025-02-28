from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import User

router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message,
    command: CommandObject,
    session: AsyncSession,
    state: FSMContext,
    user: User,
):
    if not user:
        user = User(
            id_user=message.from_user.id,
            username=message.from_user.username,
        )
        session.add(user)
        await session.commit()
    await message.answer(text="Привет, я Remi")
