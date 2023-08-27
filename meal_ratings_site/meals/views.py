from django.shortcuts import render,redirect,get_object_or_404
from .models import Meal, MealRating
from django.db.models import Avg
from .forms import MealForm,SortForm
from datetime import timedelta
from django.utils import timezone
from django.http import Http404

def index(request):
    # 評価が4.5以上の条件を付け加える。もし評価が4.5以上のデータが3つ以上なかったら、その条件を省く
    avg_rating_threshold = 4.5
    top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).filter(avg_rating__gte = avg_rating_threshold).order_by('-avg_rating')[:3]
    
    if len(top3_list) < 3:
        top3_list = Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating')[:3]
    
    # 現在の日付から90日以内の条件を付け加える。もしデータが3つ以上なかったら、その条件を省いた最近追加した順にする
    ninety_days_ago = timezone.now() - timedelta(days=90)
    recently_added_list = Meal.objects.all().filter(dateAdded__range=[ninety_days_ago, timezone.now()]).order_by('-dateAdded')[:3]
    
    if len(recently_added_list) < 3:
        recently_added_list = Meal.objects.all().order_by('-dateAdded')[:3]
        
    morning_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.morning)[:3]
    afternoon_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.afternoon)[:3]
    evening_foods_list = Meal.objects.filter(typicalMealTime = Meal.MealTime.evening)[:3]
    
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

def returnFoodsList(category):
    if category == "morning":
        return Meal.objects.filter(typicalMealTime = Meal.MealTime.morning)
    elif category == "afternoon":
        return Meal.objects.filter(typicalMealTime = Meal.MealTime.afternoon)
    elif category == "evening":
        return Meal.objects.filter(typicalMealTime = Meal.MealTime.evening)
    elif category == "top_rated":
        return Meal.objects.annotate(avg_rating=Avg('mealrating__rating')).order_by('-avg_rating')
    elif category == "recently_added":
        return  Meal.objects.all().order_by('-dateAdded')
    
def returnTitle(category):
    if category == "morning":
        return "Morning"
    elif category == "afternoon":
        return "Afternoon"
    elif category == "evening":
        return "Evening"
    elif category == "top_rated":
        return "Top Rated"
    elif category == "recently_added":
        return "Recently Added"
    else:
        raise Http404("Poll does not exist")
    
def category(request, category):
    foods_list = returnFoodsList(category)
        
    if request.method == 'GET':  
        selected_order = request.GET.get('order')
        
        if selected_order == 'rating':
            foods_list =  foods_list.annotate(average_rating=Avg('mealrating__rating')).order_by('-average_rating')  
        elif selected_order == 'country':
            foods_list = foods_list.order_by('countryOfOrigin')
        elif selected_order == 'date':
            foods_list = foods_list.order_by('-dateAdded')
        else:
            foods_list
        
        form = SortForm(initial={'choice_field': selected_order})
        context = {
            'foods_list':foods_list,
            'form':form,
            'title': returnTitle(category)
        }
    
    return render(request, 'meals/category.html',context)

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