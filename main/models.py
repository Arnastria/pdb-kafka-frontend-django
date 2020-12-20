from django.db import models
import datetime

# Create your models here.
class ProductRating(models.Model):
    clothing_id = models.CharField('Clothing id',max_length=120, primary_key=True)
    age = models.CharField('Age',max_length=120)
    title = models.CharField('Title',max_length=120)
    review = models.CharField('Review',)
    rating = models.IntegerField('Rating')
    recommended = models.IntegerField('Recommended')
    positive_feedback = models.IntegerField('Positive Feedback')
    division = models.CharField('Division')
    department = models.CharField('Department')
    class_name = models.CharField('Class name',max_length=120)

    @classmethod
    def create(cls, cloth_id, age, review, rating, recommended, positive_feedback, division, department, class_name):
        productRating = cls(clothing_id=cloth_id, age=age, review= review, rating=rating, recommended=recommended, positive_feedback= positive_feedback, division=division,department=department, class_name=class_name)
        return productRating

class AverageAge(models.Model):
    avg_id = models.CharField('avg_a_id',primary_key=True)
    average_age = models.IntegerField('Average Age')
    timestamp = models.DateTimeField()

    @classmethod
    def create(cls, avg_id, average_age, timestamp):
        avg_age = cls(avg_id=avg_id, average_age=average_age, timestamp=timestamp)
        return avg_age

class AverageRating(models.Model):
    avg_id = models.CharField('avg_r_id',primary_key=True)
    average_rating = models.IntegerField('Average Rating')
    timestamp = models.DateTimeField()

    @classmethod
    def create(cls, avg_id, average_rating, timestamp):
        avg_rating = cls(avg_id=avg_id, average_rating=average_rating, timestamp=timestamp)
        return avg_rating