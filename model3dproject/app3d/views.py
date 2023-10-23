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

    # if request.method == "POST":
    #     form = Model3dForm(request.POST, request.FILES, instance=model3d)
    #     if form.is_valid():
    #         form.save()  # Enregistrez les modifications dans la base de données
    #         return redirect("home")  # Redirigez vers la page d'accueil ou une autre page

    # else:
    #     form = Model3dForm(instance=model3d)
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







# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import Model3dForm  # Assurez-vous d'importer le bon formulaire depuis votre application

# def model_update(request, id):
#     model3d = get_object_or_404(Model3d, id=id)
    
#     if request.method == "POST":
#         form = Model3dForm(request.POST, request.FILES, instance=model3d)
#         if form.is_valid():
#             # Modifiez les champs qui ne sont pas dans le formulaire ici
#             model3d.champ1 = "Nouvelle valeur pour champ1"
#             model3d.champ2 = "Nouvelle valeur pour champ2"
#             # Enregistrez les modifications dans la base de données
#             model3d.save()
#             return redirect("home")  # Redirigez vers la page d'accueil ou une autre page

#     else:
#         form = Model3dForm(instance=model3d)
#     return render(request, "app3d/model-update.html", context={"model3d": model3d})
