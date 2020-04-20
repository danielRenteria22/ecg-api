from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from .User import User

class UserEcg(MongoModel):
    points = fields.ListField(fields.FloatField(min_value = 0))
    category = fields.IntegerField(default = None)
    created_at = fields.DateTimeField()
    correct_classification = fields.BooleanField(default = None,blank=True)
    image_url = fields.CharField()
    user_id = fields.referenceField(User, ,blank=True)
    use = fields.CharField(choices=('TRAINING', 'TESTING'))