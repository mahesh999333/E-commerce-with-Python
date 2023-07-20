from rest_framework.views import APIView
from shared.schema_validator import ProductSchema
from shared.helper import *
from shared.constants import *




class AddProduct(APIView):
    def post(self, request):
        try:
            product_schema = ProductSchema(**request.data)
            vendor_id = product_schema.vendor_id
            vendor = get_vendor_object({'id':vendor_id, 'type':UserType.VENDOR})
            product = Product.objects.create(
                title=product_schema.title,
                category=product_schema.category,
                quantity=product_schema.quantity,
                description=product_schema.description,
                brand=product_schema.brand,
                selling_price=product_schema.selling_price,
                vendor_id=[vendor_id]
            )
            return respond(
                code=RespondCode.CODE_201.value,
                message=RespondMessage[201],
                response_data=product_schema.dict()
            )
        except Exception as e:
            xprint(e)
            return respond(
                code=RespondCode.CODE_400.value,
                message=RespondMessage[4000],
                response_data=product_schema.errors()
            )

    def get(self, request):
        try:
            filter_data = {
                key: value
                for key, value in request.GET.items()
                if value
            }
            filter_data.pop("user_id", None)
            products = get_products(filter_data)
            products = products.to_mongo().to_dict()
            # del products['_id'], products['vendor_id']
            products['_id'] = str(products['_id'])
            products['vendor_id'] = str(products['vendor_id'])
            return respond(
                code=RespondCode.CODE_200.value,
                message=RespondMessage[200],
                response_data=products
            )
        except Exception as e:
            xprint(e)
            return respond(
                code=RespondCode.CODE_400.value,
                message=RespondMessage[4000]
            )
            
