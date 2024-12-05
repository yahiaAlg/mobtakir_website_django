# views.py
from pprint import pprint
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    messages.success(request, "Login successful!")

                    next_url = request.GET.get("next")
                    if next_url:
                        return redirect(next_url)
                    return redirect("chatbot:chat")
                else:
                    messages.error(request, "Invalid username or password.")
            except Exception as e:
                print(f"Login error: {str(e)}")
                messages.error(request, "Login failed! Please try again.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()

    return render(request, "registration/login.html", {"form": form})


def register_view(request):
    # If user is already authenticated, redirect to chat
    if request.user.is_authenticated:
        return redirect("chatbot:chat")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Registration successful!")

                # Handle redirect URL
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("chatbot:chat")
            except Exception as e:
                pprint(f"Registration error: {str(e)}")
                messages.error(request, "Registration failed! Please try again.")
                return redirect("register")
        else:
            # If form is invalid, add form errors as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "registration/register.html", {"form": form})
    else:
        # GET request - show empty form
        form = CustomUserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def dashboard(request):
    return render(request, "registration/dashboard.html")
