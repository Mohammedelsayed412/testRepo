from django import forms
from products.models import Products



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'