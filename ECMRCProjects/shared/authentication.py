from django.core.exceptions import PermissionDenied
import jwt
from ECMRCProject.settings import get_secret, AUTHENTICATION_EXCLUDED_URLS
from shared.helper import *
from shared.constants import *
import json



class UserAunthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path_info in AUTHENTICATION_EXCLUDED_URLS:
                return self.get_response(request)
            
            decoded_token = jwt.decode(
                request.headers['Authorization'],
                get_secret("TOKEN_SECRET_KEY"),
                get_secret("ALGORITHM")
            )
            user_id = decoded_token["user_id"]
            user = get_user({"id":user_id})
            
            if not user :
                return respond(
                    code=RespondCode.CODE_401.value,
                    message=RespondMessage[4001]
                )
                
            request.user = user
            request.decoded_token = decoded_token
            print(">>>>>>>User Authenticated<<<<<<<")
            
            self.authorization_middleware(request)
        except jwt.DecodeError:
            print(">>>>>Invalid token<<<<<<")
            return respond(
                code=RespondCode.CODE_401.value,
                message=RespondMessage[4001]
            )
        except Exception as e:
            print(">>>>>Invalid token<<<<<<")
            xprint(e)
            return respond(
                code=RespondCode.CODE_406.value,
                message=RespondMessage[4006]
            )
             
            
    def authorization_middleware(self, request):
        try:
            user_id = request.GET.get('user_id')
            if not user_id:
                request_data = json.loads(request.body)
                user_id = request_data.get("user_id")
            if not user_id == request.decoded_token["user_id"]:
                return respond(
                    code=RespondCode.CODE_403.value,
                    message=RespondMessage[4003]
                )
            print(">>>>>>>User Authorized<<<<<<<")
        except Exception as e:
            xprint(e)
            raise PermissionDenied("You do not have permission to perform this action.")
    
