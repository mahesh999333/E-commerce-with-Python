from rest_framework.views import APIView
from rest_framework import permissions
from shared.schema_validator import *
from shared.constants import *
from shared.helper import *
import json
from passlib.hash import bcrypt

class UserSignUp(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            validated_data = UserSchema(**request.data)
            username = request.data.get("username")
            password = request.data.get("password")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            mobile = request.data.get("mobile")
            address_1 = request.data.get("address_1")
            address_2 = request.data.get("address_2")
            zip_code = request.data.get("zip_code")
            city = request.data.get("city")
            state = request.data.get("state")
            country = request.data.get("country")
            type = request.data.get("type")
            
            address_data = {
                "address_1":address_1,
                "zip_code":zip_code,
                "city":city,
                "state":state,
                "country":country
            }
            if address_2:
                address_data["address_2"]=address_2
            address = create_address_object(address_data)
            address = address.to_mongo().to_dict()
            
            user_data = {
                "user_name":username,
                "password":password,
                "first_name":first_name,
                "last_name":last_name,
                "mobile":mobile,
                "type":type.upper(),
                "address":[address]
            }
            user = create_user_object(user_data)
            if not user:
                response_body = "User Registration Done"
                return respond(code=RespondCode.CODE_201.value,
                               message=RespondMessage[201],
                               response_data=response_body
                               )
                
            # user = user.to_mongo().to_dict()
            # json_data = json.dumps(user, default=str)
            # json_data = json.loads(json_data)
            
        except Exception as e:
            xprint(e)
            return respond(
                code=RespondCode.CODE_400.value,
                message=RespondMessage[4000],
                response_data=e
                )
        
        
        
class UserLogin(APIView):
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = get_user({'user_name':username})
        
        if not user:
            response_body = {
                "username":username, 
                "password":password
            }
            return respond(
                code=RespondCode.CODE_404.value,
                message=RespondMessage[4004],
                response_data=response_body
            )
        
        is_password_correct = bcrypt.verify(password, user.hashed_password)
        
        if not is_password_correct:
            response_body={
                "username":username, 
                "password":password
            }
            return respond(
                code=RespondCode.CODE_400.value,
                message=RespondMessage[4001],
                response_data=response_body
            )
        try:
            user_id = str(user.id)
            # user_id = json.dumps(user_id)
            token = generate_jwt_token(user_id)
        except Exception as e:
            xprint(e)
            return respond(code=RespondCode.CODE_400.value, message=RespondMessage[4000])
        
        response_body = "User Logged In Successfully"
        return respond(
            code=RespondCode.CODE_200.value,
            message=RespondMessage[200],
            response_data=response_body,
            header = token
        )