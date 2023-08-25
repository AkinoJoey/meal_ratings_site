from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('morning/', views.morning, name='morning'),
    path('meals/<slug:meal_slug>', views.meal_detail, name='detail'),
]