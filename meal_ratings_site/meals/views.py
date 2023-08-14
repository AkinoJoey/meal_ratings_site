from django.shortcuts import render
from django.http import HttpResponse
from .models import Meal
from django.db.models import Avg


def index(request):
    top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating').values('name', 'imageUrl')[:3]
    recently_added_list = Meal.objects.all().order_by('-dateAdded').values('name', 'imageUrl')[:3]
    
    morning = 1
    afternoon = 2
    evening = 3
    
    morning_foods_list = Meal.objects.filter(typicalMealTime = morning).values('name','imageUrl')[:3]
    afternoon_foods_list = Meal.objects.filter(typicalMealTime = afternoon).values('name','imageUrl')[:3]
    evening_foods_list = Meal.objects.filter(typicalMealTime = evening).values('name','imageUrl')[:3]
    
    context = {
        'top3_list': top3_list,
        'recently_added_list' : recently_added_list,
        'morning_foods_list':morning_foods_list,
        'afternoon_foods_list':afternoon_foods_list,
        'evening_foods_list':evening_foods_list
    }
    return render(request, "meals/index.html", context)
