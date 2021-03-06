from django.db import models
from itertools import chain
import datetime

# Create your models here.
class PdbModels(models.Model):

    def to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data
    
    class Meta:
        abstract = True


class ProductRating(PdbModels):
    clothing_id = models.CharField('Clothing id',max_length=120, primary_key=True)
    age = models.CharField('Age',max_length=120)
    title = models.CharField('Title',max_length=120)
    review = models.CharField('Review',max_length=1024)
    rating = models.IntegerField('Rating')
    recommended = models.IntegerField('Recommended')
    positive_feedback = models.IntegerField('Positive Feedback')
    division = models.CharField('Division',max_length=255)
    department = models.CharField('Department',max_length=255)
    class_name = models.CharField('Class name',max_length=120)

    @classmethod
    def create(cls, cloth_id, age, review, rating, recommended, positive_feedback, division, department, class_name):
        productRating = cls(clothing_id=cloth_id, age=age, review= review, rating=rating, recommended=recommended, positive_feedback= positive_feedback, division=division,department=department, class_name=class_name)
        return productRating

class AverageAge(PdbModels):
    avg_id = models.CharField('avg_a_id',max_length=120,primary_key=True)
    average_age = models.IntegerField('Average Age')
    timestamp = models.DateTimeField()

    @classmethod
    def create(cls, avg_id, average_age, timestamp):
        avg_age = cls(avg_id=avg_id, average_age=average_age, timestamp=timestamp)
        return avg_age

class AverageRating(PdbModels):
    avg_id = models.CharField('avg_r_id',max_length=120,primary_key=True)
    average_rating = models.IntegerField('Average Rating')
    timestamp = models.DateTimeField()

    @classmethod
    def create(cls, avg_id, average_rating, timestamp):
        avg_rating = cls(avg_id=avg_id, average_rating=average_rating, timestamp=timestamp)
        return avg_rating