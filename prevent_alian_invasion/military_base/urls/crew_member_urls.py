from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from military_base.views import crew_member_views as views



urlpatterns = [
    path('', views.getCrewMembers, name="crewmembers"),
    path('create/', views.createCrewMember, name="crewmember_create"),
    path('<str:pk>/', views.getCrewMemberById, name="crewmember_id"),
    path('update/<str:pk>/', views.updateCrewMember, name="crewmember_update"),
    path('move/<str:pk>/', views.moveCrewMember, name="crewmember_move"),
    path('delete/<str:pk>/', views.deleteCrewMember, name="crewmember_delete"),
]