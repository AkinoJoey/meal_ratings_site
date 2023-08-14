from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Meal
from django.db.models import Avg
from .forms import MealForm

def index(request):
    if request.method == 'GET':
        top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating').values('name', 'imageUrl')[:3]
        recently_added_list = Meal.objects.all().order_by('-dateAdded').values('name', 'imageUrl')[:3]
        
        morning = 1
        afternoon = 2
        evening = 3
        
        morning_foods_list = Meal.objects.filter(typicalMealTime = morning).values('name','imageUrl')[:3]
        afternoon_foods_list = Meal.objects.filter(typicalMealTime = afternoon).values('name','imageUrl')[:3]
        evening_foods_list = Meal.objects.filter(typicalMealTime = evening).values('name','imageUrl')[:3]
        
        form = MealForm()
        
        context = {
            'top3_list': top3_list,
            'recently_added_list' : recently_added_list,
            'morning_foods_list':morning_foods_list,
            'afternoon_foods_list':afternoon_foods_list,
            'evening_foods_list':evening_foods_list,
            'form':form
        }
        
    else:
        form = MealForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    return render(request, "meals/index.html", context)
