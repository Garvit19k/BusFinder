# app urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get_bus/', views.GetBus, name="GetBus"),
    path('get_all_bus/', views.GetAllBus, name="GetallBus"),
    path('get_route/', views.GetRoute, name="Getroute"),
    path('bus_initial/<int:initial_loc>/', views.BusInitial, name="GetBusInitial"),
    path('bus_final/<int:final_loc>/', views.Busfinal, name="GetBusfinal"),
    path('get_destination/<str:dest_str>/', views.GetDesinations, name="GetDestination"),
    path('add_click/', views.AddClick, name="Add_Click"),
    path('bus_extra_detail/',views.GetBusExtra,name="Bus_details"),
    path('bulk_destination/',views.CreateBulkDestination,name="Bulk_destination"),
    path('bulk_bus/',views.CreateBulkBus,name="Bulk_bus"),
]
