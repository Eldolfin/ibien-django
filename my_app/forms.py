from django import forms
from .models import Sell

class SellForm(forms.ModelForm):
    class Meta:
        model = Sell
        exclude = ['seller', 'pub_date', 'location']
