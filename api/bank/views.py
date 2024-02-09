from rest_framework import generics
from .models import Loan
from .serializers import LoanSerialzaer
from accounts.permissions import IsStaff, ReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerialzaer
    permission_classes = [ReadOnly | IsStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['duration', 'interest_rate', 'interval']