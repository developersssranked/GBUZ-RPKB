from aiogram.fsm.state import StatesGroup, State


class ContactInformationOurOrgState(StatesGroup):
    organization: str = State()
    full_name: str = State()
    motive: str = State()
    post: str = State()
    subdivision: str = State()
    reason_of_petition: str = State()
    car_brand: str = State()
    car_color: str = State()
    car_number: str = State()
    phone_number: str = State()
    dop_data: str = State()
    reciepent_fullName: str = State()