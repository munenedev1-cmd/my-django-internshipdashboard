from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import InternshipApplicationForm, RegistrationForm


def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("apply")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back.")
                return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def application_view(request):
    application = getattr(request.user, "internship_application", None)
    if request.method == "POST":
        form = InternshipApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.email = request.user.email or form.cleaned_data["email"]
            obj.save()
            messages.success(request, "Your internship application has been submitted successfully.")
            return redirect("dashboard")
    else:
        form = InternshipApplicationForm(instance=application)

    return render(request, "application.html", {"form": form, "application": application})


@login_required
def dashboard(request):
    application = getattr(request.user, "internship_application", None)
    status_steps = application.get_progress_steps() if application else []
    return render(request, "dashboard.html", {"application": application, "status_steps": status_steps})
