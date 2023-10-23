from django.shortcuts import render, get_object_or_404, redirect
from .models import Model3d
from django.contrib.auth import get_user_model, login, logout, authenticate

# Create your views here.

def home(request):
    models3d = Model3d.objects.all()
    return render(request, 'app3d/home.html', context={'models3d': models3d})

def detail(request, id):
    model3d = get_object_or_404(Model3d, id=id)
    model3d.views += 1
    model3d.save()
    return render(request, 'app3d/detail.html', context={'model3d': model3d})


def model_update(request, id):
    model3d = get_object_or_404(Model3d, id=id)
    return render(request, "app3d/model-update.html", context={"model3d": model3d})


def user_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = get_user_model().objects.create(username=username, password=password)
        login(request,user)
        return redirect("home")
    return render(request, "app3d/signup.html")

def user_logout(request):
    logout(request)
    return redirect("home")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "app3d/login.html")

