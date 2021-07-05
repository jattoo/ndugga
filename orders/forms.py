from django import forms
from localflavor.us.forms import USZipCodeField
from localflavor.gb.forms import GBPostcodeField
from .models import Order


    
class OrderCreateForm(forms.ModelForm):
    
    post_code = USZipCodeField() 
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'post_code', 'city']