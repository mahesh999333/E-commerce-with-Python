from rest_framework.response import Response
from shared.models import *
import jwt
from datetime import datetime, timedelta
from mongoengine import Q
from ECMRCProject.settings import get_secret
from django.shortcuts import get_object_or_404
from django.utils.decorators import decorator_from_middleware



def apply_middleware(middleware_class):
    """
    Decorator to apply middleware to specific APIs or URLs.
    """
    return decorator_from_middleware(middleware_class)



def respond(code, message, response_data=None, header=None):
    response_body = {
        "message" : message,
        "response_data":response_data
    }
    http_status_code = code
    if header:
        header ={"AUTHORIZATION" :'Bearer ' + header  }
    return Response(response_body, http_status_code, content_type='application/json', headers=header)


def xprint(value):
    print("********************************************************")
    print(value)
    print("********************************************************")


def create_address_object(data):
    return Address(**data)

def create_user_object(data):
    return User.objects.create(**data)

def get_user(filter):
    return User.objects.filter(**filter).first()

def generate_jwt_token(user_id):
    payload = {
        "user_id" : user_id,
        "exp" : datetime.now() + timedelta(days=3)
    }
    token = jwt.encode(payload, get_secret("TOKEN_SECRET_KEY"), get_secret("ALGORITHM"))
    return token

# def get_vendor_object(filter):
#     return User.objects.filter(**filter).first()

def create_product_object(data):
    return Product.objects.create(**data)

def get_vendor_object(filter_obj):
    queryset = User.objects.filter(**filter_obj)
    vendor = get_object_or_404(queryset)
    return vendor

def get_products(filter_obj):
    # queryset = Q(**{f'{key}__icontains': value} for key, value in filter_obj.items())
    queryset = Q()
    for key, value in filter_obj.items():
        queryset |= Q(**{f'{key}__icontains': value})

    queryset = Product.objects.filter(queryset)
    products = get_object_or_404(queryset)
    return products
