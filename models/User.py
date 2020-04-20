from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

class User(MongoModel):
    name = fields.CharField()
    email = fields.CharField()
    password = fields.CharField()
    isAuthorized = fields.BooleanField(default = False)
    