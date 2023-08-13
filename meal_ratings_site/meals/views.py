from django.shortcuts import render
from django.http import HttpResponse
from .models import Meal, MealRating
from django.db.models import Avg



def index(request):
    top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating').values('name', 'imageUrl')[:3]
    context = {
        "top3_list": top3_list
    }
    return render(request, "meals/index.html", context)
