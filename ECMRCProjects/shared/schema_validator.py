from pydantic import BaseModel, conint, constr, validator
from typing import Optional
from bson import ObjectId
from shared.validators import *


class UserSchema(BaseModel):
    username: constr(strip_whitespace=True, min_length=1)
    password: constr(strip_whitespace=True, min_length=8, max_length=16)
    first_name: constr(strip_whitespace=True, min_length=1)
    last_name: constr(strip_whitespace=True, min_length=1)
    mobile: constr(strip_whitespace=True, min_length=10, max_length=14)
    address_1: constr(strip_whitespace=True, min_length=1)
    address_2: Optional[constr(strip_whitespace=True, min_length=1)]
    zip_code: conint(strict=True)
    city: constr(strip_whitespace=True, min_length=1)
    state: constr(strip_whitespace=True, min_length=1)
    country: constr(strip_whitespace=True, min_length=1)
    type: constr(strip_whitespace=True, min_length=1)
    
    @validator('zip_code')
    def validate_zip_code(cls, value):
        return zip_code_validation(value)
    
    @validator('username', 'first_name', 'last_name')
    def validate_string(cls, value):
        return string_validation(value)
        
    @validator('password')
    def validate_password(cls, value):
        return password_validation(value)
    
    @validator('mobile')
    def validate_mobile(cls, value):
        return mobile_validation(value)


class ProductSchema(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)
    category: constr(strip_whitespace=True, min_length=1)
    quantity: conint(strict=True)
    description: constr(strip_whitespace=True, min_length=1)
    brand: constr(strip_whitespace=True, min_length=1)
    selling_price: conint(strict=True)
    vendor_id : str
    
    @validator('title', 'description', 'category', 'brand')
    def validate_alphanum_string(cls, value):
        return alphanum_string_validation(value)
    
    @validator('quantity', 'selling_price')
    def validate_quantity(cls, value):
        return num_validation(value)
    
    @validator('vendor_id')
    def validate_object_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid vendor_id')
        return value
        

class CartSchema(BaseModel):
    product_id : str
    
    @validator('product_id')
    def validate_object_id(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid product_id: {value}")
        return value