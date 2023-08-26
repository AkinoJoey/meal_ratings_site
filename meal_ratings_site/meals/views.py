from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Meal, MealRating
from django.db.models import Avg
from .forms import MealForm,SortForm
from django.core import serializers
from django.core.serializers import serialize
import datetime


def index(request):
    # 評価が4.5以上の条件を付け加える
    top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating').values('name', 'imageUrl')[:3]
    # 現在の日付から90日以内の条件を付け加える
    recently_added_list = Meal.objects.all().order_by('-dateAdded').values('name', 'imageUrl')[:3]
    
    morning = 1
    afternoon = 2
    evening = 3
    
    morning_foods_list = Meal.objects.filter(typicalMealTime = morning).values('name','imageUrl')[:3]
    afternoon_foods_list = Meal.objects.filter(typicalMealTime = afternoon).values('name','imageUrl')[:3]
    evening_foods_list = Meal.objects.filter(typicalMealTime = evening).values('name','imageUrl')[:3]
    
    
    if request.method == 'GET':
        form = MealForm()
        
    elif request.method == 'POST':
        form = MealForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('index')
            
    context = {
            'top3_list': top3_list,
            'recently_added_list' : recently_added_list,
            'morning_foods_list':morning_foods_list,
            'afternoon_foods_list':afternoon_foods_list,
            'evening_foods_list':evening_foods_list,
            'form':form
    }
    return render(request, "meals/index.html", context)

def morning(request):
    morning_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.morning)
        
    if request.method == 'GET':  
        selected_order = request.GET.get('order')
        
        if selected_order == 'rating':
            morning_foods_list =  morning_foods_list.annotate(average_rating=Avg('mealrating__rating')).order_by('-average_rating')  
        elif selected_order == 'country':
            morning_foods_list = morning_foods_list.order_by('countryOfOrigin')
        elif selected_order == 'date':
            morning_foods_list = morning_foods_list.order_by('-dateAdded')
        else:
            morning_foods_list
        
        form = SortForm(initial={'choice_field': selected_order})
        context = {
            'morning_foods_list':morning_foods_list,
            'form':form,
        }
    
    return render(request, 'meals/morning.html',context)


def meal_detail(request, meal_slug):
    meal = get_object_or_404(Meal, slug=meal_slug)
    
    if request.method == 'GET':
        
        context = {
            'meal':meal
        }
        
    elif request.method == 'POST':
        meal_instance = Meal.objects.get(slug = meal_slug)
        rating = request.POST.get('rating')
        rating_instance = MealRating(meal=meal_instance,rating=rating)
        rating_instance.save()
        
        return redirect(request.path)
        
    return render(request,'meals/meal_detail.html',context)