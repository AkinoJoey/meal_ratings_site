from django.db import models
from django.db.models import Avg
import datetime

class Meal(models.Model):
    class MealTime(models.IntegerChoices):
        morning = 1,
        afternoon = 2,
        evening = 3
        
    name = models.CharField(max_length=255)
    description = models.TextField()
    imageUrl = models.ImageField(upload_to='meals/')
    countryOfOrigin = models.CharField(max_length=255)
    typicalMealTime = models.IntegerField(choices=MealTime.choices)
    dateAdded = models.DateTimeField(default=datetime.datetime.now())
        
    def __str__(self):
        return self.name
    
    def avgRating(self):
        return self.mealrating_set.aggregate(Avg("rating"))["rating__avg"]
    
    def numberOfVotes(self):
        return self.mealrating_set.count()

class MealRating(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE)
    rating = models.FloatField()
    dateOfRating = models.DateTimeField(default=datetime.datetime.now())
