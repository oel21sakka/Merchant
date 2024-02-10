from django.urls import path
from .views import OperationView, InstallmentView, TransactionView, payview, approve_view

urlpatterns = [
    path('', OperationView.as_view()),
    path('installment/', InstallmentView.as_view()),
    path('transaction/', TransactionView.as_view()),
    path('pay/', payview),
    path('approve/', approve_view),
]