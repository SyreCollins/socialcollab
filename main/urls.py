from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("login", views.Login, name="login"),
    path("register", views.Register, name="register"),
    path("dashboard", views.Dashboard, name="dashboard")
]
