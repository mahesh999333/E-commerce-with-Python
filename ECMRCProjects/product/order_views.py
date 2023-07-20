from rest_framework.views import APIView
from shared.schema_validator import ProductSchema
from shared.helper import *
from shared.constants import *
import json
from shared.authentication import UserAunthenticationMiddleware



# @apply_middleware(UserAunthenticationMiddleware)


# class OrderAPI(APIView):
#     def post(self, request):
#         try:
            
#         except Exception as e:
#             xprint(e)
#             return respond(
#                 code=RespondCode.CODE_400.value,
#                 message=RespondMessage[400]
#             )