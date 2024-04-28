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
    [InlineKeyboardButton(text='ГБУЗ РБ РПКБ', callback_data='our_org')],
    [InlineKeyboardButton(text='Стороняя организация', callback_data='not_our_org')],
    ])


def get_answer_keyboard(user_chat_id):
    answer_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Ответить', callback_data=f'answer_{user_chat_id}')],
        ])

    return answer_keyboard