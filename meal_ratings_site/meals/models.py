from django.db import models
import datetime

class Meal(models.Model):
    class MealTime(models.IntegerChoices):
        morning = 1,
        afternoon = 2,
        evening = 3
        
    name = models.CharField(max_length=255)
    description = models.TextField()
    imageUrl = models.ImageField()
    countryOfOrigin = models.CharField(max_length=255)
    typicalMealTime = models.IntegerField(MealTime.choices)
    dateAdded = models.DateTimeField(default=datetime.datetime.now())
        
    def __str__(self):
        return self.name

class MealRating(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE)
    rating = models.FloatField()
    dateOfRating = models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return self.meal.name