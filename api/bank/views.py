from rest_framework import generics, filters
from .models import Loan
from .serializers import LoanSerialzaer
from accounts.permissions import IsStaff, ReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class LoanView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerialzaer
    permission_classes = [ReadOnly | IsStaff]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['duration', 'interest_rate', 'interval']
    ordering_fields = '__all__'