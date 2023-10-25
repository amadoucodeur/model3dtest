from django.shortcuts import render, get_object_or_404, redirect
from .models import Model3d, Badge
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import Model3dForm
from django.db.models import F
from django.http import JsonResponse

User = get_user_model()
# Create your views here.

def home(request):
    models3d = Model3d.objects.all()
    return render(request, 'app3d/home.html', context={'models3d': models3d})


def detail(request, id):
    model3d = get_object_or_404(Model3d, id=id)

    # Augmentez le compteur de vues
    Model3d.objects.filter(id=model3d.id).update(views=F('views') + 1)
    
    user = model3d.user
    if not user.has_badge("Star") and model3d.views >= 1000:
        badge, _ = Badge.objects.get_or_create(name="Star", description="Le modèle d'un utilisateur a plus de 1k vues")
        user.badges.add(badge)

    if not user.has_badge("Pioneer") and user.is_pioneer():
        badge, _ = Badge.objects.get_or_create(name="Pioneer", description="L'utilisateur est inscrit depuis plus d'un an")
        user.badges.add(badge)

    return render(request, 'app3d/detail.html', context={'model3d': model3d})


def model_delete(request, id):
    model3d = get_object_or_404(Model3d, id=id)
    model3d.delete()
    return redirect('home')  

def model_add(request):
    if request.method == "POST":
        form = Model3dForm(request.POST, request.FILES)
        if form.is_valid():
            model3d = form.save(commit=False)
            model3d.user = request.user
            model3d.save()
            return redirect('detail', id=model3d.id)

    form = Model3dForm()
    return render(request, "app3d/model-add.html", {'form': form})


def model_update(request, id):
    model3d = get_object_or_404(Model3d, id=id)

    if not request.user.has_perm('app3d.change_model3d', model3d):
        return redirect('detai', id=id)  # Redirigez vers une vue d'autorisation non accordée

    if request.method == "POST":
        form = Model3dForm(request.POST, request.FILES, instance=model3d)
        if form.is_valid():
            form.save()
            return redirect('detail', id=id)

    form = Model3dForm(instance=model3d)
    context = {
        'model3d': model3d,
        'form': form,
    }
    return render(request, "app3d/model-update.html", context=context)


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
        if user := authenticate(username=username, password=password):
            login(request, user)
            user = request.user
            return redirect("home")
    return render(request, "app3d/login.html")


def user_badges_api(request, username):
    user = get_object_or_404(User, username=username)
    badges = user.badges.all()
    badge_data = [{'name': badge.name, 'description': badge.description} for badge in badges]

    return JsonResponse(badge_data, safe=False)