from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.defaultfilters import slugify
import datetime
import os

class Meal(models.Model):
    class MealTime(models.IntegerChoices):
        morning = 1,
        afternoon = 2,
        evening = 3
        
    name = models.CharField(max_length=255)
    description = models.TextField()
    imageUrl = models.ImageField()
    countryOfOrigin = models.CharField(max_length=255)
    typicalMealTime = models.IntegerField(choices=MealTime.choices)
    dateAdded = models.DateTimeField(default=datetime.datetime.now())
    slug = models.SlugField(null=True, unique=True)
        
    def __str__(self):
        return self.name
    
    def avgRating(self):
        return self.mealrating_set.aggregate(Avg("rating"))["rating__avg"]
    
    def numberOfVotes(self):
        return self.mealrating_set.count()

    def save(self, *args, **kwargs):
        self.set_slug()
    
        # pkを取得するために1度保存
        super().save(*args, **kwargs)
        self.set_imageUrl()
        return super().save(*args, **kwargs)
    
    def set_imageUrl(self):
        old_filename = self.imageUrl.name
        extension = old_filename.split('.')[-1]
        new_filename = f'{self.pk}.{extension}'  
        
        if old_filename != new_filename:
            self.imageUrl = new_filename  
            self.rename_image_name(old_filename, new_filename)
        
    def rename_image_name(self,old_filename, new_filename):
        old_path = os.path.join(settings.MEDIA_ROOT, old_filename) 
        new_path = os.path.join(settings.MEDIA_ROOT, new_filename)
        os.rename(old_path, new_path)
        
    def set_slug(self):
        if self.slug is None:
            self.slug = slugify(self.name)
    
class MealRating(models.Model):
    meal = models.ForeignKey(Meal,on_delete=models.CASCADE)
    rating = models.FloatField()
    dateOfRating = models.DateTimeField(default=datetime.datetime.now())
