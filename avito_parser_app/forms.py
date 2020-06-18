from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'title',
            'price',
            'currency',
            'url',
        )
        widgets = {
            'title': forms.TextInput(),
            'currency': forms.TextInput(),
        }
