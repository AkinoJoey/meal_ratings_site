from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('category/<slug:category>', views.category, name='category'),
    path('meals/<slug:meal_slug>', views.meal_detail, name='detail'),
]