from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    #path("asset/<int:id>/", views.asset, name="asset"),
    #path("<int:id>/", views.asset, name="asset"),
    path("add/", views.add, name="add"),
    path("edit/<int:pk>/", views.edit, name="edit"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("register/", views.register, name="register"),
    #path("collect/", views.collect, name="collect"),
]