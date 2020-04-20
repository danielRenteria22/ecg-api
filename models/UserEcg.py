from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from .User import User

class UserEcg(MongoModel):
    points = fields.ListField(fields.FloatField(min_value = 0))
    category = fields.IntegerField(default = None)
    created_at = fields.DateTimeField()
    correct_classification = fields.BooleanField(default = None,blank=True)
    image_url = fields.CharField()
    user_id = fields.ReferenceField(User)
    use = fields.CharField(choices=('TRAINING', 'TESTING'))