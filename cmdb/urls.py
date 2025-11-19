from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("asset/<int:id>/", views.asset, name="asset"),
    #path("<int:id>/", views.asset, name="asset"),
    path("add/", views.add, name="add"),
    path("edit/<int:pk>/", views.edit, name="edit"),
    path("delete/<int:pk>/", views.delete, name="delete"),
    #path("collect/", views.collect, name="collect"),
]