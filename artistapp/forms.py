from django import forms
from adminapp import models
from adminapp.models import Product 

class ProductForm(forms.ModelForm):  
    class Meta:
        model = Product  
        fields = "__all__"  