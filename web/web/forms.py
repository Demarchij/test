from django import forms

class RegisterForm(forms.Form):
	username = forms.CharField(max_length = 127, label = 'Username')
	password = forms.CharField(max_length = 255, label = 'Password', widget=forms.PasswordInput())
	email = forms.CharField(max_length = 255, label = 'Email')
	phone = forms.CharField(max_length = 20, required = False, label = 'Phone')

class LoginForm(forms.Form):
	username = forms.CharField(required = True, max_length = 127, label = 'Username')
	password = forms.CharField(required = True, max_length = 255, label = 'Password', widget=forms.PasswordInput())

class ItemForm(forms.Form):
	title = forms.CharField(required = True, max_length = 127, label = 'Title')
	tags = forms.CharField(max_length=127, label = 'Tags')
	filename = forms.CharField(required = True, max_length=255, label = 'Filename')
	category = forms.CharField(max_length=127, label = 'Category')
	description = forms.CharField(max_length = 255, label = 'Description')




