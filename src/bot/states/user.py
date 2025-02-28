from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    add_tasks = State()


class AdminState(StatesGroup):
    any_state = State()
