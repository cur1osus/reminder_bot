from aiogram import Router


def setup_message_routers() -> Router:
    from . import (
        cmd_add_tasks,
        cmd_my_reminders,
        cmd_start,
        del_remind,
        unknown_message,
    )

    router = Router()
    router.include_router(cmd_start.router)
    router.include_router(cmd_add_tasks.router)
    router.include_router(cmd_my_reminders.router)
    router.include_router(del_remind.router)
    router.include_router(unknown_message.router)
    # router.include_router(errors.router)

    return router
