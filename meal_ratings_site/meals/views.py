from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Meal, MealRating
from django.db.models import Avg
from .forms import MealForm,SortForm
from django.core import serializers
from django.core.serializers import serialize
from datetime import timedelta
from django.utils import timezone


def index(request):
    # 評価が4.5以上の条件を付け加える。もし評価が4.5以上のデータが3つ以上なかったら、その条件を省く
    avg_rating_threshold = 4.5
    top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).filter(avg_rating__gte = avg_rating_threshold).order_by('-avg_rating').values('name', 'imageUrl')[:3]
    
    if len(top3_list) < 3:
        top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating').values('name', 'imageUrl')[:3]
    
    # 現在の日付から90日以内の条件を付け加える。もしデータが3つ以上なかったら、その条件を省いた最近追加した順にする
    ninety_days_ago = timezone.now() - timedelta(days=90)
    recently_added_list = Meal.objects.all().filter(dateAdded__range=[ninety_days_ago, timezone.now()]).order_by('-dateAdded').values('name', 'imageUrl')[:3]
    
    if len(recently_added_list) < 3:
        recently_added_list = Meal.objects.all().order_by('-dateAdded').values('name', 'imageUrl')[:3]

    
    morning_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.morning).values('name','imageUrl')[:3]
    afternoon_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.afternoon).values('name','imageUrl')[:3]
    evening_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.evening).values('name','imageUrl')[:3]
    
    
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