from django import forms
from django.contrib.auth.models import User 
from .models import Profile

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(label="Password", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

  class Meta:
    model = User 
    fields = ("username", "first_name", "email")

  def clean_password2(self):
    cd = self.cleaned_data
    if cd["password"] != cd["password2"]:
      raise forms.ValidationError("Passwords dont't match.")

    return cd["password2"]


# Allows users to edit the attributes of the built-in Django User model
class UserEditForm(forms.ModelForm):
  class Meta:
    model = User 
    fields = ("first_name", "last_name", "email")


# Allows users to edit the profile data that they save in the custom Profile model
class ProfileEditForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ("date_of_birth", "photo")