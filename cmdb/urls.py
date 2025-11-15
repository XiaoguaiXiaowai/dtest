from django.urls import path
from . import views

urlpatterns = [
    path("", views.cmdb, name="cmdb"),
    #path("asset/<int:id>/", views.asset, name="asset"),
    #path("<int:id>/", views.asset, name="asset"),
    #path("add/", views.add, name="add"),
    #path("collect/", views.collect, name="collect"),
]