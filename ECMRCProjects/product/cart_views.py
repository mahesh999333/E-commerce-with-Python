from rest_framework.views import APIView
from shared.schema_validator import CartSchema
from shared.helper import *
from shared.constants import *




class AddToCart(APIView):
    def post(self, request):
        try:
            validated_data = CartSchema(request.data)
            product_id = request.data.get('product_id')
            product = get_products({'id':product_id})
            
            product = product.to_mongo().to_dict()
            product['_id'] = str(product['_id'])
            product['vendor_id'] = str(product['vendor_id'])
            
            return respond(
                code=RespondCode.CODE_200.value,
                message=RespondMessage[200],
                response_data=product
            )
        except Exception as e:
            xprint(e)
            response_body = {
                "e" : str(e)
            }
            return respond(
                code=RespondCode.CODE_400.value,
                message=RespondMessage[400],
                response_data=response_body
            )