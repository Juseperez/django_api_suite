from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("dasdboard/", views.dasdboard, name="dasdboard"),
]