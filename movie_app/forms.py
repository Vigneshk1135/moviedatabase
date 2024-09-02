# forms.py

from django import forms
from .models import Movie, Category

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'poster', 'description', 'actors', 'release_date', 'youtube_link', 'category']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.py

from django import forms
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
