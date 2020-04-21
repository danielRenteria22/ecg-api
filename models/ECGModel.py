from pymodm import fields, MongoModel, EmbeddedMongoModel

class ECGModel(MongoModel):
    points = fields.ListField(fields.FloatField(min_value = 0))
    category = fields.IntegerField(default = None)
    created_at = fields.DateTimeField()
    correct_classification = fields.BooleanField(default = None)
    use = fields.CharField(choices=('TRAINING', 'TESTING'))