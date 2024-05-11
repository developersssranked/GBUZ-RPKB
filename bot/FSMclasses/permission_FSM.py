from aiogram.fsm.state import StatesGroup, State


class PermissionState(StatesGroup):
    username: str = State()
