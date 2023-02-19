from django import forms
from .models import Sell

class SellForm(forms.ModelForm):
    """The form for the Sell model.
       It is what links the model to the view.
       And allows the user to input data into the model.
       Either to create or update an entry."""
    class Meta:
        model = Sell
        exclude = ['seller', 'pub_date', 'location']
