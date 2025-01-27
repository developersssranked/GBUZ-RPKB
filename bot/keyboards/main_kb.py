from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder



keyboard_del = ReplyKeyboardRemove()


def get_accept_or_close_keyboard(user_chat_id):


    accept_or_close_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Принять', callback_data=f'accept_{user_chat_id}')],
        [InlineKeyboardButton(text='Отклонить', callback_data=f'close_{user_chat_id}')],
        ])

    return accept_or_close_keyboard

choose_organization = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Заявка на пропуск автомобиля сотрудника', callback_data='our_org')],
    [InlineKeyboardButton(text='Въезд на территорию стороняя организация', callback_data='not_our_org')],
    ])


def get_answer_keyboard(user_chat_id):
    answer_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ответить', callback_data=f'answer_{user_chat_id}')],
        ])

    return answer_keyboard


def get_status_user_keyboard(user_chat_id):
    status_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Разрешить доступ', callback_data = f'okay-{user_chat_id}')],
        [InlineKeyboardButton(text='Запретить доступ', callback_data = f'not_okay-{user_chat_id}')],
    ])
    return status_keyboard


def get_change_user_status_keyboard(username):

    change_user_status_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Разрешить', callback_data = f'status-1-{username}')],
        [InlineKeyboardButton(text='Запретить', callback_data = f'status-0-{username}')],
    ])
    return change_user_status_keyboard
