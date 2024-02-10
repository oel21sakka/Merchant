from rest_framework import serializers
from .models import Operation, Installment, Transaction
from .models import OperationType, DurationType, IntervalType, InstallmentType

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['type'] = InstallmentType(data['type']).label
        return data

class OperationSerializer(serializers.ModelSerializer):
    installments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    due_day = serializers.IntegerField(min_value=1, max_value=28)

    class Meta:
        model = Operation
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only':True}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['installments'] = InstallmentSerializer(instance.installments, many=True).data
        data['type'] = OperationType(data['type']).name
        data['pay_duration'] = DurationType(data['pay_duration']).label
        data['receive_duration'] = DurationType(data['receive_duration']).label
        data['pay_interval'] = IntervalType(data['pay_interval']).label
        data['receive_interval'] = IntervalType(data['receive_interval']).label
        return data

    def create(self, validated_data):
        operation = super().create(validated_data)
        installments = operation.get_installments()
        for installment in installments:
            installment['operation']=operation
            Installment.objects.create(**installment)
        return operation

    def validate(self, attrs):
        pay_interval = attrs.get('pay_interval')
        pay_duration = attrs.get('pay_duration')
        if pay_interval > pay_duration:
            raise serializers.ValidationError("pay_duration must be longer than pay_interval")
        type = attrs.get('type')
        pay_date = attrs.get('pay_date')
        receive_date = attrs.get('receive_date')
        if type == OperationType.Loan and pay_date<receive_date:
            raise serializers.ValidationError("pay_date must be later than receive_date")
        if type == OperationType.Fund and pay_date>receive_date:
            raise serializers.ValidationError("receive_date must be later than pay_date")
        return attrs