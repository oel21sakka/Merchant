from rest_framework import serializers
from .models import Loan, Bank

class LoanSerialzaer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    def get_available(self, obj):
        return Bank.objects.first().is_available(obj.max_amount+obj.max_amount*obj.interest_rate/100)

    def validate(self, attrs):
        min_amount = attrs.get('min_amount')
        max_amount = attrs.get('max_amount')
        if min_amount>max_amount:
            raise serializers.ValidationError("min_amount mustn't be bigger than max_amount")
        return attrs

    class Meta:
        model = Loan
        fields='__all__'