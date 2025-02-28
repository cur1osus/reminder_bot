import datetime

import aioschedule
from sqlalchemy import select

from db import Reminder, Weekday
from init_bot import bot
from init_db import _sessionmaker


async def send_message(id_user, message, schedule: aioschedule):
    await bot.send_message(chat_id=id_user, text=message)
    return schedule.CancelJob


async def set_tasks_func(schedule: aioschedule):
    async with _sessionmaker() as session:
        reminders = await session.scalars(
            select(Reminder).where(Reminder.is_set.is_(False))
        )
        if not reminders:
            return
        for reminder in reminders:
            now = datetime.datetime.now()
            weekday = str(now.weekday() + 1)
            if (
                reminder.repeat not in [Weekday.EVERYDAY.value, Weekday.ONE_TIME.value]
                and weekday not in reminder.repeat
            ):
                continue
            hour, minute = reminder.time_to_send.split(":")
            schedule.every().day.at(f"{hour}:{minute}").do(
                send_message,
                id_user=reminder.user.id_user,
                message=reminder.message,
                schedule=schedule,
            )
            reminder.is_set = True
            if Weekday.ONE_TIME.value in reminder.repeat:
                await session.delete(reminder)
        await session.commit()
