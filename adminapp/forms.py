# forms.py
from django import forms
from .models import Categorymodel

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categorymodel
        fields = ['Category', 'Image']
        widgets = {
            'Category': forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
            'Image': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'margin-bottom: 10px;'}),
        }

