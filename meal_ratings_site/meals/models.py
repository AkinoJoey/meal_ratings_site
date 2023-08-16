from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import datetime
import os


class Meal(models.Model):
    class MealTime(models.IntegerChoices):
        morning = 1,
        afternoon = 2,
        evening = 3
        
    name = models.CharField(max_length=255)
    description = models.TextField()
    imageUrl = models.ImageField(upload_to='images/')
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

# インスタンスを保存してpkが作成された後に、imageUrlをpkにupdateする
@receiver(post_save, sender=Meal)
def set_meal_image_url(sender, instance, **kwargs):
    Meal.objects.filter(pk=instance.pk).update(imageUrl=f'images/{instance.pk}.jpg')

# インスタンスを保存して、pkが作成された後に、uploadされた画像の名前を変更する
@receiver(post_save, sender=Meal)
def rename_meal_image(sender, instance, **kwargs):
    if instance.imageUrl:
        old_path = instance.imageUrl.path
        new_filename = f'{instance.pk}.jpg'
        new_path = os.path.join(settings.MEDIA_ROOT, 'images', new_filename)
        
        if old_path != new_path:
            os.rename(old_path, new_path)
            instance.imageUrl.name = f'images/{new_filename}'
            instance.save(update_fields=['imageUrl'])