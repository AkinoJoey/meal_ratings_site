from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'imageUrl', 'countryOfOrigin', 'typicalMealTime', 'description']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({
            'class': 'uk-input',
            'id': 'name',
            'placeholder': 'Hamburger',
            'required': 'required',  
        })
        
        self.fields['imageUrl'].widget.attrs.update({
            'class': 'uk-input',
            'id': 'image-url',
            'required': 'required',  
        })
        
        self.fields['countryOfOrigin'].widget.attrs.update({
            'class': 'uk-input',
            'id': 'country-of-origin',
            'placeholder': 'Germany',
            'required': 'required',  
        })
        
        self.fields['typicalMealTime'].widget.attrs.update({
            'class': 'uk-select',
            'id': 'typical-meal-time',
            'required': 'required', 
        })
        
        self.fields['description'].widget.attrs.update({
            'class': 'uk-input',
            'id': 'description',
            'placeholder': 'Sandwich made with ground beef patty',
            'required': 'required',  
        })
