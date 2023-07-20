from django.http import JsonResponse
from datetime import datetime

# Error Response

class ErrorResponse:
    def __init__(self):
        self.timestamp = datetime.now()
        self.code = None
        self.status = None
        self.message = None
        self.data = None
        self.errors = []

    class ValidationError:
        def __init__(self, field, message):
            self.field = field
            self.message = message

    def add_validation_error(self, field, message):
        self.errors.append(self.ValidationError(field, message))

    def to_json_response(self):
        response = {
            'timestamp': self.timestamp.strftime('%d-%m-%Y %H:%M:%S'),
            'code': self.code,
            'status': self.status,
            'message': self.message,
            'data': self.data,
            'errors': [
                {'field': error.field, 'message': error.message}
                for error in self.errors
            ]
        }
        return JsonResponse(response)

    def from_http_status(self, http_status, message, data=None):
        self.code = http_status.value
        self.status = http_status.name
        self.message = message
        self.data = data


# GlobalExceptionHandler.java

from django.http import JsonResponse
from rest_framework.exceptions import APIException

class WorkerIdNotFoundException(APIException):
    status_code = 404
    default_detail = "Worker ID not found."
    default_code = "not_found"


class FinormicStatusRecordNotFound(APIException):
    status_code = 404
    default_detail = "Finormic Login record doesn't exist."
    default_code = "not_found"


class GlobalExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except APIException as e:
            return self.handle_api_exception(e)
        except Exception as e:
            return self.handle_generic_exception(e)

        return response

    def handle_api_exception(self, exception):
        error_response = {
            'code': exception.status_code,
            'status': exception.default_code,
            'message': str(exception)
        }
        return JsonResponse(error_response, status=exception.status_code)

    def handle_generic_exception(self, exception):
        error_response = {
            'code': 500,
            'status': 'internal_server_error',
            'message': 'Internal Server Error.'
        }
        return JsonResponse(error_response, status=500)


