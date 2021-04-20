from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm

def user_login(request):
  # Check if the form was submitted
  if request.method == "POST":
    form = LoginForm(request.POST)

    # Check if the form is valid
    if form.is_valid():
      cd = form.cleaned_data

      # Authenticate the user's credentials
      user = authenticate(request, username=cd["username"], password=cd["password"])

      if user is not None:

        # Check if the user have an active account
        if user.is_active:
          login(request, user)  # Sets the user's session and logs him/her in
          return HttpResponse("Authenticated Successfully")
        else:
          return HttpResponse("Disabled Account")

      else:
        return HttpResponse("Invalid Login")

  else:   # request.method == "GET"
    form = LoginForm()

  return render(request, "account/login.html", {"form": form})


@login_required
def dashboard(request):
  return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
  if request.method == "POST":
    user_form = UserRegistrationForm(request.POST)

    if user_form.is_valid():
      # Create a new user object, but avoid saving it just yet
      new_user = user_form.save(commit=False)

      # Set the chosen password
      new_user.set_password(user_form.cleaned_data["password"])

      # Officially save the User Object
      new_user.save()

      return render(request, "account/register_done.html", {"new_user": new_user})
  else:   # method == "GET"
    user_form = UserRegistrationForm()

  return render(request, "account/register.html", {"user_form": user_form})