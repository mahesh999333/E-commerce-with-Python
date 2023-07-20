from mongoengine import connect

connect(
    db='<database_name>',
    host='<mongodb_host>',
    username='<mongodb_username>',
    password='<mongodb_password>',
    authentication_source='<mongodb_authentication_source>'
)
