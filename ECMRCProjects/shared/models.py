from mongoengine import BooleanField, DateTimeField, \
    DictField, Document as MongoDocument, EmbeddedDocument, \
    EmbeddedDocumentField, EnumField, IntField, ListField,\
    ReferenceField, StringField, ListField
    
from passlib.hash import bcrypt
from .constants import *


class Address(EmbeddedDocument):
    # user_id = ReferenceField(dbref=True)
    address_1 = StringField(required=True)
    address_2 = StringField()
    zip_code = IntField(reqiured=True)
    city = StringField(required=True)
    state = StringField(required=True)
    country = StringField(required=True)

class User(MongoDocument):
    user_name = StringField(required=True, unique=True)
    password = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    address = ListField(EmbeddedDocumentField(Address))
    mobile = StringField(required=True, unique=True)
    hashed_password = StringField(required=True)
    type = EnumField(UserType)
    
    def set_password(self, password):
        self.hashed_password = bcrypt.hash(password)
        
    def check_password(self, password):
        return bcrypt.verify(password, self.hashed_password)
    
    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.set_password(self.password)
            # Clear the plain text password
            # self.password = None
        super().save(*args, **kwargs)
 
 
class Vendor(MongoDocument):
    # product_list = ListField(ReferenceField(Product))
    company_name = StringField()
    shop_name = StringField(required=True)
    shop_number = IntField()
    shop_owner_name = StringField(required=True)
    contact_number = IntField(required=True)
    address = EmbeddedDocumentField(Address)
    
    
class Product(MongoDocument):
    title = StringField(required=True)
    category = StringField(required=True)
    quantity = IntField(default=1)
    description = StringField()
    selling_price = IntField(required=True)
    descounted_price = IntField()
    brand = StringField(required=True)
    # descount_id = ReferenceField(dbref=True)
    vendor_id = ListField(ReferenceField(Vendor))
    

class Payment(MongoDocument):
    type = StringField()
    allowed = BooleanField(default=True)


class Order(MongoDocument):
    user_id = ReferenceField(User, dbref=True)
    # discount_id = ReferenceField(dbref=True)
    payment_id = ReferenceField(Payment, bref=True)
    product = ListField(ReferenceField(Product, bref=True))
    total_price = IntField()
    status = EnumField(OrderStatus)
    shipping_address = StringField(required=True)
    order_date = DateTimeField()
    
    
class Cart(MongoDocument):
    user_id = ReferenceField(User ,dbref=True)
    items = ListField(DictField())
      
    
# class Review(MongoDocument):
#     user_id = ReferenceField(User, dbref=True)
#     seller_id = ReferenceField(Vendor, dbref=True)
#     product_id = ReferenceField(Product, dbref=True)
    # rating = FloatField()
    # review_text = StringField()
    
    # class ValidationError(Exception):
    #     pass

    # def clean(self):
    #     if not (0 <= self.my_float <= 5):
    #         raise self.ValidationError("Value must be between 0 and 5.")