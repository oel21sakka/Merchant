from rest_framework import serializers
from .models import Loan, Bank

class LoanSerialzaer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    def get_available(self, obj):
        return Bank.objects.first().is_available(obj.max_amount+obj.max_amount*obj.interest_rate/100)

    class Meta:
        model = Loan
        fields='__all__'