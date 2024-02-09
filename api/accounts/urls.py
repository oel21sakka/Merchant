from django.urls import path
from .views import add_staff

urlpatterns = [
    path('add-staff/', add_staff),
]
