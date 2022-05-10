from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from military_base.views import mothership_views as views



urlpatterns = [
    path('', views.getMotherShips, name="motherships"),
    path('create/', views.createMotherShip, name="mothership_create"),
    path('<str:pk>/', views.getMotherShipById, name="mothership_id"),
    path('update/<str:pk>/', views.updateMotherShip, name="mothership_update"),
    path('delete/<str:pk>/', views.deleteMotherShip, name="mothership_delete"),

]