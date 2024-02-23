from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

# class ItemsForm(forms.ModelForm):
#     class Meta:
#         model = Items
#         fields = ['name','image', 'price', 'is_active']
# #

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
class IdNumber(forms.Form):
    id = forms.IntegerField(initial=0)
    count = forms.IntegerField(initial=0)
	
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class InfoForm(forms.ModelForm):
    class Meta:
        model = TotalSale
        fields = ("customer_name", "ph_no",)