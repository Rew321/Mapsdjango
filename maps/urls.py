from django.urls import path
from .views import *



urlpatterns =[
    path("", HomeView.as_view(), name= "home"),
    path("geododing/<int:pk>", GeocodingView.as_view(), name= "geocoding"),
    path("distance", DistanceView.as_view(), name= "distance"),
    path("map", MapView.as_view(), name= "map")
]
