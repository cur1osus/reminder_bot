from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


router = Router()
flags = {"throttling_key": "default"}


@router.message(flags=flags)
async def any_unknown_message(message: Message, state: FSMContext) -> None:
    await message.answer(text="не понимаю тебя :(")


@router.callback_query()
async def any_unknown_callback(query: CallbackQuery) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
