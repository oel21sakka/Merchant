from django.urls import path
from .views import LoanView

urlpatterns = [
    path('loan/', LoanView.as_view()),
]
