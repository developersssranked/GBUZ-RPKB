from aiogram import Router

from aiogram import F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command


from bot.FSMclasses.main_FSM import ContactInformationOurOrgState
from bot.FSMclasses.permission_FSM import PermissionState
from bot.FSMclasses.p2p_messaging_FSM import AnswerToUser
from bot.keyboards.main_kb import choose_organization,get_accept_or_close_keyboard,get_answer_keyboard, get_status_user_keyboard, get_change_user_status_keyboard
from bot.utils import utils
from database import db

import os


router = Router()


@router.message(F.text == '/start')
async def start(message:Message, bot: Bot, state: FSMContext):
    await state.clear()
    if message.from_user.username is not None:

        if not db.is_exist_user(message.from_user.username):
            
            users_data = {
                'username' : message.from_user.username,
                'chat_id' : message.from_user.id
                }
            
            db.insert_user_DB(users_data=users_data)
            await bot.send_message(os.getenv('ADMIN_CHAT_ID'),f'Пользователь @{ message.from_user.username } запустил бота', reply_markup = get_status_user_keyboard(message.from_user.id)) #TODO добавить клавиатуру админу
            await bot.send_message(message.from_user.id, 'Ваша заявка на использование бота отправлена. Вы получите уведомление после ее рассмотрения')
        
        else:

            if db.get_user_status(username = message.from_user.username)==1:


                await message.answer('Здравствуйте!\nВыберите нужный вариант',reply_markup=choose_organization)

    else:
        await message.answer('Здравствуйте!\nПеред использованием бота пожалуйста установите username в профиле.')


    

@router.callback_query(F.data == 'our_org')
async def our_org(call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)
    await call.message.answer('Введите фамилию, имя, отчество заявителя')

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
    
    await message.answer('Введите цель заезда')
    await state.set_state(ContactInformationOurOrgState.motive)

@router.message(ContactInformationOurOrgState.motive)
async def get_motive(message: Message, bot: Bot, state: FSMContext):

    motive = message.text.strip()


    await state.update_data(motive = motive)
    
    await message.answer('Введите вашу фамилию, имя, отчество')
    await state.set_state(ContactInformationOurOrgState.full_name)


@router.message(ContactInformationOurOrgState.full_name)
async def get_full_name(message: Message, bot: Bot, state: FSMContext):

    full_name = message.text.strip()
    await state.update_data(full_name = full_name)

    data = await state.get_data()
    
    if data['organization'] == 'ГБУЗ РБ РКПБ':
        
        await message.answer('Ввведите фамилию, имя, отчество получателя')
        await state.set_state(ContactInformationOurOrgState.reciepent_fullName)
        
    
    else:
        await message.answer('Введите марку и модель автомобиля')
        await state.set_state(ContactInformationOurOrgState.car_brand)

@router.message(ContactInformationOurOrgState.reciepent_fullName)  # Только для ГБУЗ РКПб
async def get_reciepentfullName(message: Message, bot: Bot, state: FSMContext):
    reciepent_fullName = message.text.strip()

    await state.update_data(reciepent_fullName = reciepent_fullName)

    await message.answer('Введите должность сотрудника, получающего пропуск')
    await state.set_state(ContactInformationOurOrgState.post)


    
@router.message(ContactInformationOurOrgState.post)  # Только для ГБУЗ РКПб
async def get_post(message: Message, bot: Bot, state: FSMContext):

    post = message.text.strip()
    await state.update_data(post = post)

    
    await message.answer('Введите название подразделения')
    await state.set_state(ContactInformationOurOrgState.subdivision)
        



@router.message(ContactInformationOurOrgState.subdivision)
async def get_subdivision(message: Message, bot: Bot, state: FSMContext):

    subdivision = message.text.strip()
    await state.update_data(subdivision = subdivision)
    
    await message.answer('Введите причину обращения.\nЕсли хотите оставить пустым, то отправьте «.»')
    await state.set_state(ContactInformationOurOrgState.reason_of_petition)


@router.message(ContactInformationOurOrgState.reason_of_petition)
async def get_reason_of_petition(message: Message, bot: Bot, state: FSMContext):

    reason_of_petition = message.text.strip()
    
    if reason_of_petition == '.':
        reason_of_petition = 'Не указана'

    await state.update_data(reason_of_petition = reason_of_petition)
    
    await message.answer('Введите марку и модель автомобиля')
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

   

    try:

        if await utils.validate_car_number(car_number):

            
            await state.update_data(car_number = car_number)

            
            if data['organization'] == 'ГБУЗ РБ РКПБ':

                await message.answer('Введите ваш номер сотового телефона')

                await state.set_state(ContactInformationOurOrgState.phone_number)
        
            else:

                await message.answer('Введите дополнительную информация. \nЕсли хотите пропустить напишите «.»')
                await state.set_state(ContactInformationOurOrgState.dop_data)

        else:
            
            await message.answer('Номер автомобиля в неверном формате. Введите номер автомобиля в формате X999XX999')
            await state.set_state(ContactInformationOurOrgState.car_number)
    except:
        await message.answer('Номер автомобиля в неверном формате. Введите номер автомобиля в формате X999XX999')
        await state.set_state(ContactInformationOurOrgState.car_number)
        

@router.message(ContactInformationOurOrgState.dop_data)    #Только для сторонней организации
async def get_phone_number(message: Message, bot: Bot, state: FSMContext):

    dop_data = message.text.strip()

    if dop_data == '.':
        dop_data = 'Не указано'

    await state.update_data(dop_data = dop_data)
    
    data = await state.get_data()


    message_to_admin = f'Пользователь: @{message.from_user.username}\nНазвание организации: {data["organization"]}\nЦель заезда: {data["motive"]}\nФИО заявителя: {data["full_name"]}\nМарка автомобиля: {data["car_brand"]}\nЦвет автомобиля: {data["car_color"]}\nГос. номер автомобиля: {data["car_number"]}\nДополнительные сведения: {data["dop_data"]}'

    await message.answer('Спасибо! Ваша заявка принята в обработку,когда ее рассмотрят вам сообщат результат.')
    await bot.send_message(chat_id=os.getenv('ADMIN_CHAT_ID'),text=message_to_admin, reply_markup=get_accept_or_close_keyboard(message.from_user.id))



        
        
@router.message(ContactInformationOurOrgState.phone_number)
async def get_phone_number(message: Message, bot: Bot, state: FSMContext):

    phone_number = message.text.strip()
    try:

        if await utils.validate_phone_number(phone_number):
        
            await state.update_data(phone_number = phone_number)

            data = await state.get_data()
            await message.answer('Спасибо! Ваша заявка принята в обработку,когда ее рассмотрят вам сообщат результат.')

            message_to_admin = f'Пользователь: @{message.from_user.username}\nНазвание организации: {data["organization"]}\nФИО заявителя: {data["full_name"]}\nФИО получателя: {data["reciepent_fullName"]}\nДолжность: {data["post"]}\nПодразделение: {data["subdivision"]}\nПричина обращения: {data["reason_of_petition"]}\nМарка автомобиля: {data["car_brand"]}\nЦвет автомобиля: {data["car_color"]}\nГос. номер автомобиля: {data["car_number"]}\nЛичный номер сотового телефона: {data["phone_number"]}'

            await bot.send_message(chat_id=os.getenv('ADMIN_CHAT_ID'),text=message_to_admin, reply_markup=get_accept_or_close_keyboard(message.from_user.id))
        else:
            
            await message.answer('Номер телефона в неверном формате.')
            await state.set_state(ContactInformationOurOrgState.phone_number)
    except Exception as ex:
        await message.answer('Номер телефона в неверном формате.')
        await state.set_state(ContactInformationOurOrgState.phone_number)

        

#Работа с админом (принятие / отклонение заявки)

@router.callback_query(lambda call: 'accept' in call.data)
async def accept (call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)

    user_chat_id = int(call.data.split('_')[1])


    await bot.send_message(chat_id = user_chat_id, text = 'Ваша заявка одобрена')

    await bot.send_message(chat_id=os.getenv("ADMIN_CHAT_ID"),text='Заявка одобрена',reply_markup=get_answer_keyboard(user_chat_id))




@router.callback_query(lambda call: 'close' in call.data)
async def close (call: CallbackQuery, bot: Bot, state: FSMContext):

    await bot.answer_callback_query(call.id)

    user_chat_id = int(call.data.split('_')[1])

    await bot.send_message(chat_id = user_chat_id, text = 'Ваша заявка отклонена')

    await bot.send_message(chat_id=os.getenv("ADMIN_CHAT_ID"),text='Заявка отклонена', reply_markup=get_answer_keyboard(user_chat_id))
    



#Работа с админом (ответ пользователю)
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


@router.callback_query(lambda call: ('okay' in call.data) and ('not' not in call.data))
async def set_user_status_1(call: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(call.id)
    
    user_chat_id = int (call.data.split('-')[-1])

    db.update_user_status(chat_id = user_chat_id, status = 1)

    await bot.send_message(call.from_user.id, 'Доступ пользователю разрешен')

    await bot.send_message(int(user_chat_id),'Ваша заявка на использование бота одобрена')

@router.callback_query(lambda call: 'not_okay' in call.data)
async def set_user_status_0(call: CallbackQuery, bot: Bot):

    await bot.answer_callback_query(call.id)
    
    user_chat_id = int (call.data.split('-')[-1])

    db.update_user_status(chat_id = user_chat_id, status = 0)

    await bot.send_message(call.from_user.id, 'Доступ пользователю запрещен')
    


    

@router.message(Command('status'))
async def set_users_status_by_admin(message: Message, state: FSMContext):
    
    if int(message.from_user.id) == int(os.getenv('ADMIN_CHAT_ID')):

        result_users = []

        for user in db.select_all_users_status_1_DB():
            result_users.append('@'+user[0])
        
        user_list_message_text ='Список пользователей:\n'+'\n\n'.join(result_users)

        await message.answer(user_list_message_text)
        
        await message.answer('Введите имя пользователя, которому хотите поменять статус в формате @test123')
        
        await state.set_state(PermissionState.username)

    else:
        await message.answer('У вас нет прав для использования этой команды')


@router.message(PermissionState.username)
async def get_actual_status(message: Message, bot: Bot, state: FSMContext):

    username = message.text.strip().replace('@','')

    if db.is_exist_user(username):

        status = db.get_user_status(username)

        if status == 1:
            status = 'Доступ разрешен'
        else:
            status = 'Доступ запрещен'

        await message.answer(f'Пользователь @{username}\nСтатус: {status}', reply_markup = get_change_user_status_keyboard(username))

    else:
        await message.answer('Нет пользователя с таким username')



    
@router.callback_query(lambda call: 'status' in call.data)
async def set_user_status_1(call: CallbackQuery, bot: Bot):
    await bot.answer_callback_query(call.id)

    username = call.data.split('-')[-1]

    status = int(call.data.split('-')[1])

    db.update_user_status(username=username,status=status)

    await bot.send_message(call.from_user.id, 'Статус пользователя успешно обновлен')

    


