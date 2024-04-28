from aiogram import Router

from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.FSMclasses.main_FSM import ContactInformationOurOrgState
from bot.FSMclasses.p2p_messaging_FSM import AnswerToUser
from bot.keyboards.main_kb import choose_organization,get_accept_or_close_keyboard,get_answer_keyboard
from bot.utils import utils

import os


router = Router()


@router.message(F.text == '/start')
async def start(message:Message, bot: Bot, state: FSMContext):
    await state.clear()


    await message.answer('Здравствуйте! Выберите организацию',reply_markup=choose_organization)
    

@router.callback_query(F.data == 'our_org')
async def our_org(call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)
    await call.message.answer('Введите фамилию, имя, отчество')

    await state.set_state(ContactInformationOurOrgState.full_name)
    await state.update_data(organization='ГБУЗ РБ РКПБ')


@router.callback_query(F.data == 'not_our_org')
async def not_our_org(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(call.id)

    await call.message.answer('Введите название организации')

    await state.set_state(ContactInformationOurOrgState.organization)


@router.message(ContactInformationOurOrgState.organization)
async def get_organiztion(message: Message, bot: Bot, state: FSMContext):

    organization = message.text.strip()
    await state.update_data(organization = organization)
    
    await message.answer('Введите цель заезда. Если хотите оставить пустым, то отправьте .')
    await state.set_state(ContactInformationOurOrgState.motive)

@router.message(ContactInformationOurOrgState.motive)
async def get_motive(message: Message, bot: Bot, state: FSMContext):

    motive = message.text.strip()

    if motive == '.':
        motive = 'Не указан'

    await state.update_data(motive = motive)
    
    await message.answer('Введите фамилию, имя, отчество')
    await state.set_state(ContactInformationOurOrgState.full_name)


@router.message(ContactInformationOurOrgState.full_name)
async def get_full_name(message: Message, bot: Bot, state: FSMContext):

    full_name = message.text.strip()
    await state.update_data(full_name = full_name)
    
    await message.answer('Введите должность')
    await state.set_state(ContactInformationOurOrgState.post)

    
@router.message(ContactInformationOurOrgState.post)
async def get_post(message: Message, bot: Bot, state: FSMContext):

    post = message.text.strip()
    await state.update_data(post = post)

    data = await state.get_data()

    if data['organization'] == 'ГБУЗ РБ РКПБ':


        await message.answer('Введите название подразделения')
        await state.set_state(ContactInformationOurOrgState.subdivision)
        
    else:
        await message.answer('Введите марку автомобиля')
        await state.set_state(ContactInformationOurOrgState.car_brand)



@router.message(ContactInformationOurOrgState.subdivision)
async def get_subdivision(message: Message, bot: Bot, state: FSMContext):

    subdivision = message.text.strip()
    await state.update_data(subdivision = subdivision)
    
    await message.answer('Введите причину обращения. Если хотите оставить пустым, то отправьте .')
    await state.set_state(ContactInformationOurOrgState.reason_of_petition)


@router.message(ContactInformationOurOrgState.reason_of_petition)
async def get_reason_of_petition(message: Message, bot: Bot, state: FSMContext):

    reason_of_petition = message.text.strip()
    
    if reason_of_petition == '.':
        reason_of_petition = 'Не указана'

    await state.update_data(reason_of_petition = reason_of_petition)
    
    await message.answer('Введите марку автомобиля')
    await state.set_state(ContactInformationOurOrgState.car_brand)
    



@router.message(ContactInformationOurOrgState.car_brand)
async def get_car_brand(message: Message, bot: Bot, state: FSMContext):

    car_brand = message.text.strip()
    await state.update_data(car_brand = car_brand)
    
    await message.answer('Введите цвет автомобиля')
    await state.set_state(ContactInformationOurOrgState.car_color)


@router.message(ContactInformationOurOrgState.car_color)
async def get_car_color(message: Message, bot: Bot, state: FSMContext):

    car_color = message.text.strip()
    await state.update_data(car_color = car_color)
    
    await message.answer('Введите государственный номер автомобиля в формате X999XX999')
    await state.set_state(ContactInformationOurOrgState.car_number)



@router.message(ContactInformationOurOrgState.car_number)
async def get_car_number(message: Message, bot: Bot, state: FSMContext):

    car_number = message.text.strip()

    data = await state.get_data()

   


    if await utils.validate_car_number(car_number):

        
        await state.update_data(car_number = car_number)

        
        if data['organization'] == 'ГБУЗ РБ РКПБ':

            await message.answer('Введите личный номер сотового телефона')

            await state.set_state(ContactInformationOurOrgState.phone_number)
    
        else:
            message_to_admin = f'Название организации: {data["organization"]}\nЦель заезда: {data["motive"]}\nФИО: {data["full_name"]}\nДолжность: {data["post"]}\nМарка автомобиля: {data["car_brand"]}\nЦвет автомобиля: {data["car_color"]}\nГос. номер автомобиля: {data["car_number"]}'

            await message.answer('Спасибо! Ваша заявка принята в обработку,когда ее рассмотрят вам сообщат результат.')
            await bot.send_message(chat_id=os.getenv('ADMIN1_CHAT_ID'),text=message_to_admin, reply_markup=get_accept_or_close_keyboard(message.from_user.id))

    else:
        
        await message.answer('Номер автомобиля в неверном формате. Введите номер автомобиля в формате X999XX999')
        await state.set_state(ContactInformationOurOrgState.car_number)



        
        
@router.message(ContactInformationOurOrgState.phone_number)
async def get_phone_number(message: Message, bot: Bot, state: FSMContext):

    phone_number = message.text.strip()

    if await utils.validate_phone_number(phone_number):
    
        await state.update_data(phone_number = phone_number)

        data = await state.get_data()
        await message.answer('Спасибо! Ваша заявка принята в обработку,когда ее рассмотрят вам сообщат результат.')

        message_to_admin = f'Название организации: {data["organization"]}\nФИО: {data["full_name"]}\nДолжность: {data["post"]}\nПодразделение: {data["subdivision"]}\nПричина обращения: {data["reason_of_petition"]}\nМарка автомобиля: {data["car_brand"]}\nЦвет автомобиля: {data["car_color"]}\nГос. номер автомобиля: {data["car_number"]}\nЛичный номер сотового телефона: {data["phone_number"]}'

        await bot.send_message(chat_id=os.getenv('ADMIN1_CHAT_ID'),text=message_to_admin, reply_markup=get_accept_or_close_keyboard(message.from_user.id))
    else:
        
        await message.answer('Номер телефона в неверном формате.')
        await state.set_state(ContactInformationOurOrgState.phone_number)
        

@router.callback_query(lambda call: 'accept' in call.data)
async def accept (call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)

    user_chat_id = int(call.data.split('_')[1])

    await call.message.copy_to(chat_id=os.getenv("ADMIN2_CHAT_ID"),reply_markup=get_answer_keyboard(user_chat_id))



@router.callback_query(lambda call: 'close' in call.data)
async def close (call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)

    user_chat_id = int(call.data.split('_')[1])

    await call.message.copy_to(chat_id=os.getenv("ADMIN2_CHAT_ID"),reply_markup=get_answer_keyboard(user_chat_id))


@router.callback_query(lambda call: 'answer' in call.data)
async def input_answer(call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)
    try:
        await state.clear()
    except:
        pass
    
    await call.message.answer('Введите ответ')

    user_chat_id = int(call.data.split('_')[1])

    await state.set_state(AnswerToUser.answer)
    await state.update_data(user_chat_id=user_chat_id)



@router.message(AnswerToUser.answer)
async def answer(message: Message, bot: Bot, state: FSMContext):
    answer = message.text.strip()

    data = await state.get_data()

    chat_id = data['user_chat_id']

    await bot.send_message(chat_id=chat_id, text = answer)

    


