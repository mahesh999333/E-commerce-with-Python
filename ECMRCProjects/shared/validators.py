from pydantic import PydanticValueError
import re


def string_validation(value):
    if not re.match(r'^[A-Za-z][A-Za-z]*$', value):
        raise PydanticValueError
    return value

def mobile_validation(value):
    if not re.match(r'^[0-9][0-9]*$', value):
        raise PydanticValueError
    return value

def password_validation(value):
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', value):
        raise PydanticValueError
    return value

def zip_code_validation(value):
    if not re.match(r'^\d{6}$', str(value)):
        raise PydanticValueError
    return value

def alphanum_string_validation(value):
    if not re.match(r'^[A-Za-z0-9\s]+$', value):
        raise PydanticValueError
    return value

def num_validation(value):
    if not re.match(r'^\d+$', str(value)) or value <= 0:
        raise ValueError('Invalid quantity or selling_price')
    return value