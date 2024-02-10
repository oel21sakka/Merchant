from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsStaff
from .serializers import OperationSerializer, InstallmentSerializer, TransactionSerializer
from .models import Operation, Installment, Transaction, InstallmentType
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from bank.models import Bank
from django.contrib.auth import get_user_model
User = get_user_model()

class OperationView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Operation.objects.all()
        else:
            return Operation.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    serializer_class = OperationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'approved', 'amount', 'pay_duration', 'receive_duration', 'user', 'due_day',\
        'intreset_rate', 'pay_date', 'receive_date',]
    ordering_fields = ['amount', 'intreset_rate', 'pay_date', 'receive_date']


class InstallmentView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Installment.objects.all()
        else:
            return Installment.objects.filter(operation__user = user)

    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type', 'completed', 'operation', 'amount', 'date']
    ordering_fields = ['amount', 'date']



class TransactionView(generics.ListAPIView):
    permission_classes = [IsStaff]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [ 'from_user', 'to_user', 'date']
    orderinf_fields = ['date']


@api_view(['get'])
@permission_classes([IsAuthenticated])
def payview(request):
    if not 'installment_id' in request.query_params:
        return Response({"installment_id": "this query param is required"}, status=status.HTTP_400_BAD_REQUEST)
    installment_id = request.query_params['installment_id']
    installment = get_object_or_404(Installment, id = installment_id)
    if not installment.operation.approved:
        return Response({"operation isn't approved yet"}, status=status.HTTP_400_BAD_REQUEST)
    if installment.completed:
        return Response({"installment_id": "installment already completed"}, status=status.HTTP_400_BAD_REQUEST)
    if installment.type == InstallmentType.Receive:
        if not request.user.is_staff:
            return Response({"unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if not Bank.objects.first().is_available(installment.amount):
            return Response({'Message':'out of balance'}, status=status.HTTP_400_BAD_REQUEST)
    transaction_data ={
        'amount' : installment.amount,
    }
    transaction_data['to_user'] = installment.operation.user if installment.type == InstallmentType.Receive\
        else User.objects.get(id=User.objects.filter(is_superuser=True).first().id)
    transaction_data['from_user'] = installment.operation.user if installment.type == InstallmentType.Pay\
        else User.objects.get(id=User.objects.filter(is_superuser=True).first().id)
    transaction = Transaction.objects.create(**transaction_data)
    installment.transaction = transaction
    installment.completed = True
    installment.save()
    if installment.type==InstallmentType.Receive:
        Bank.objects.first().pay(installment.amount)
    if installment.type==InstallmentType.Pay:
        Bank.objects.first().recieve(installment.amount)
    return Response(InstallmentSerializer(installment).data, status=status.HTTP_200_OK)

@api_view(['get'])
@permission_classes([IsStaff])
def approve_view(request):
    if not 'operation_id' in request.query_params:
        return Response({"operation_id": "this query param is required"}, status=status.HTTP_400_BAD_REQUEST)
    operation_id = request.query_params['operation_id']
    operation = get_object_or_404(Operation, id = operation_id)
    operation.approved = True
    operation.save()
    return Response(OperationSerializer(operation).data, status=status.HTTP_200_OK)