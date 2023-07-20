# import json
# import logging
# import uuid

# from django.http import JsonResponse
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework import status

# logger = logging.getLogger(__name__)

# class RequestInterceptorMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         request.id = str(uuid.uuid4())
#         logger.debug(f"{request.id} Interceptor preHandle id generated for request for uri {request.path} from {request.META['REMOTE_ADDR']}")
#         request.META["trace-id"] = request.id

#         auth_token = request.META.get("HTTP_AUTHORIZATION", "")

#         flag = self.check_token_and_failure(auth_token)

#         if flag:
#             return None
#         else:
#             return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)

#     def process_response(self, request, response):
#         logger.debug(
#             f"{request.META.get('trace-id')} Response sent with code = {response.status_code} for uri = {request.path} from {request.META['REMOTE_ADDR']}"
#         )
#         response.setdefault("Access-Control-Allow-Origin", "*")
#         del request.META["trace-id"]
#         logger.debug("Interceptor postHandle id cleared")
#         return response

#     def check_token_and_failure(self, auth_token):
#         if not auth_token:
#             return False

#         if not auth_token.startswith("Bearer"):
#             logger.error(f"You gave me an invalid token {auth_token}")
#             return False

#         token = auth_token.split()[1]

#         if token == mono_auth_token or token == pirimid_webhook_token:
#             return True
#         else:
#             logger.error(f"Token doesn't start with Bearer {auth_token}")
#             return False




#---------------------------------------------------------------------------------

import logging
import uuid
from functools import wraps

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

import os
import django
from django.http import HttpRequest, HttpResponse
from django.conf import settings
import requests

logger = logging.getLogger("django")

class RequestInterceptorMiddleware():
    mono_auth_token = "PYT9EwhwtRGyRq2RfiwqqrxzOLTp77r1BvXFi2IKvnHbGjLoKNF2iWw6jrQfH.aEBakazUrMJHvpBUcyZaaVM8ORcQwaUSeZmihlP5Zv3bSGYYV8J8tb8jrNN9D.DQAYeEtIhAHRWn91OeehAP4FVBBGMjCqzeazt02UazlH18LdcQeRTNHhrkPP9"
    pirimid_webhook_token = "Xn2r5u8x/A?D(G+KaPdSgVkYp3s6v9y$B&E)H@McQeThWmZq4t7w!z%C*F-JaNd"

    def __call__(self, request):
        self.process_view(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.id = uuid.uuid4()
        # logger.debug(f"{request.id} Interceptor preHandle id generated for request for uri {request.path} from {request.META['REMOTE_ADDR']}")
        self.set_trace_id(request.id)

        auth_token = request.headers.get('Authorization')

        if not self.check_token_and_failure(auth_token, request):
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    def process_response(self, request, response):
        # logger.debug(f"{request.id} Response sent with code = {response.status_code} for uri = {request.path} from {request.META['REMOTE_ADDR']}")
        self.clear_trace_id()
        logger.debug("Interceptor postHandle id cleared")
        return response

    def check_token_and_failure(self, auth_token, request):
        if not auth_token:
            # logger.error("Received a request without any token")
            return False
        else:
            if auth_token.startswith("Bearer"):
                token = auth_token[len("Bearer "):]
                if token == self.mono_auth_token or token == self.pirimid_webhook_token:
                    return True
                else:
                    logger.error(f"You gave me an invalid token {auth_token}")
                    return False
            else:
                logger.error(f"Token doesn't start with Bearer {auth_token}")
                return False

    def set_trace_id(self, trace_id):
        from logging import getLogger
        from logging.handlers import MemoryHandler

        handler = MemoryHandler(capacity=1)
        logger = getLogger()
        logger.addHandler(handler)
        logger = logging.LoggerAdapter(logger, {'trace-id': trace_id})
        handler.setTarget(logger)

    def clear_trace_id(self):
        from logging import getLogger
        from logging.handlers import MemoryHandler

        handler = MemoryHandler(capacity=1)
        logger = getLogger()
        logger.addHandler(handler)
        logger = logging.LoggerAdapter(logger, {})
        handler.setTarget(logger)



os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
settings.configure(DEBUG=True, SECRET_KEY='your-secret-key')
django.setup()


def dummy_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, World!")


middleware = RequestInterceptorMiddleware()
# middleware.mono_auth_token = "YOUR_MONO_AUTH_TOKEN"
# middleware.pirimid_webhook_token = "YOUR_PIRIMID_WEBHOOK_TOKEN"

request = requests.Request()
response = HttpResponse()

# Set the Authorization header with a valid or invalid token
request.headers['Authorization'] = 'Bearer PYT9EwhwtRGyRq2RfiwqqrxzOLTp77r1BvXFi2IKvnHbGjLoKNF2iWw6jrQfH.aEBakazUrMJHvpBUcyZaaVM8ORcQwaUSeZmihlP5Zv3bSGYYV8J8tb8jrNN9D.DQAYeEtIhAHRWn91OeehAP4FVBBGMjCqzeazt02UazlH18LdcQeRTNHhrkPP9'

# Process the request through the middleware
middleware.process_view(request, dummy_view, [], {})

# Call the dummy view function
response = dummy_view(request)

# Process the response through the middleware
middleware.process_response(request, response)
