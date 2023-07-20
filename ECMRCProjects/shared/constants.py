from enum import Enum


class RespondCode(Enum):
    #SUCCESS CODE
    CODE_200 = 200
    CODE_201 = 201
    
    #ERROR CODE
    CODE_400 = 400
    CODE_401 = 401
    CODE_403 = 403
    CODE_404 = 404
    CODE_405 = 405
    CODE_406 = 406
    
    

    
RespondMessage = {
    200 : "Success",
    201 : "Created Successfully",
    
    4000 : "Something went wrong",
    4001 : "Invalid Credentials",
    4002 : "User not found",
    4003 : "Authorization Failed",
    4004 : "Data not found",
    4005 : "Something went wrong during Authorization",
    4006 : "Invalid Token",
    
    6001 : "Something went wrong while user authentication",
    6002 : "Something went wrong while user authorization",
    6003 : "Vendor not found"
}


class OrderStatus(Enum):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    DISPATCH = "DISPATCH"
    DELIVERED = "DELIVERED"
    
class UserType(Enum):
    CUSTOMER  = "CUSTOMER"
    VENDOR = "VENDOR"