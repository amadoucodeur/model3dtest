from django.urls import path
from .views import (
    home,
    detail,
    user_signup,
    user_logout,
    user_login,
    model_update,
    model_add,
    model_delete,
    user_badges_api,
)

# app_name = 'app3d'

urlpatterns = [
    path("",home, name="home"),
    path("<int:id>/",detail, name="detail"),
    path("<int:id>/update/", model_update, name="model-update"),
    path("add/", model_add, name="model-add"),
    path("delete/<int:id>/", model_delete, name="model-delete"),
    path("signup/",user_signup, name="signup"),
    path("logout/",user_logout, name="logout"),
    path("login/",user_login, name="login"),
    path('api/user_badges/<str:username>/', user_badges_api, name='user-badges-api'),

]
