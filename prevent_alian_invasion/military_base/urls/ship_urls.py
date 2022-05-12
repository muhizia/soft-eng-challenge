from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from military_base.views import ship_views as views



urlpatterns = [
    path('', views.getShips, name="ships"),
    path('create/', views.createShip, name="ship_create"),
    path('<str:pk>/', views.getShipById, name="ship_id"),
    path('update/<str:pk>/', views.updateShip, name="ship_update"),
    path('delete/<str:pk>/', views.deleteShip, name="ship_delete"),
]