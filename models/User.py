from pymodm import connect, fields, MongoModel, EmbeddedMongoModel

class User(MongoModel):
    name = fields.CharField()
    email = fields.CharField()
    password = fields.CharField()
    isAuthorized = fields.BooleanField(default = False)

    def toJson(self):
        selfDict = self.to_son().to_dict()
        selfDict['id'] = str(selfDict['_id'])
        del selfDict['_id']

        return selfDict
