from aiogram.fsm.state import StatesGroup, State


class AnswerToUser(StatesGroup):
    user_chat_id: str = State()
    answer: str = State()