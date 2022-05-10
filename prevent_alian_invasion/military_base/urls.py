from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from military_base import views



urlpatterns = [
    path('', views.getMotherShips, name="motherships"),
    path('create/', views.createMotherShip, name="mothership-create"),
    path('<str:pk>/', views.getMotherShipById, name="mothership-id"),
    path('update/<str:pk>/', views.updateMotherShip, name="mothership-update"),
    path('delete/<str:pk>/', views.deleteMotherShip, name="mothership-delete"),

]