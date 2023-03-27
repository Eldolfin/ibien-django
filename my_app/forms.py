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

    # validate the price making sure it's strictly positive
    def clean(self):
        cleaned_data = super(SellForm, self).clean()
        price = cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be superior to 0")
