

async def validate_car_number(car_number: str) -> bool:

    if (len(car_number)==9):
        if (car_number[0].isalpha()) and (car_number[1].isnumeric()) and (car_number[2].isnumeric()) and (car_number[3].isnumeric()) and (car_number[4].isalpha()) and (car_number[5].isalpha()) and (car_number[6].isnumeric()) and (car_number[7].isnumeric()) and (car_number[8].isnumeric()):
            return True
    
    return False


async def validate_phone_number(phone_number: str) -> bool:

    if (((len(phone_number)==11) and (phone_number.startswith('8'))) or (len(phone_number) == 12 and phone_number.startswith('+'))):
        return True
    else:
        return False