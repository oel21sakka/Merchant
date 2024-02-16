from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from datetime import date
from bank.choices import InstallmentType, IntervalType, DurationType, OperationType

class Operation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField(choices = OperationType)
    amount = models.DecimalField(max_digits = 14, decimal_places = 2)
    interest_rate = models.DecimalField(max_digits = 5, decimal_places = 2)
    pay_date = models.DateField()
    receive_date = models.DateField()
    pay_duration = models.IntegerField(choices=DurationType)
    receive_duration = models.IntegerField(choices=DurationType)
    pay_interval = models.IntegerField(choices = IntervalType)
    receive_interval = models.IntegerField(choices = IntervalType)
    due_day = models.IntegerField()
    approved = models.BooleanField(default = False)

    def get_installments(self):
        installments=[]
        pay_installment_count = self.pay_duration//self.pay_interval
        pay_amount = (self.amount + (self.amount*self.interest_rate/100 if self.type==OperationType.Loan else 0))
        pay_installment_amount = round(pay_amount / pay_installment_count, 2)
        year_value, month_value = self.pay_date.year, self.pay_date.month
        for _ in range(pay_installment_count):
            installments.append(
                {
                "type": InstallmentType.Pay,
                "amount": pay_installment_amount,
                "date": date(year_value,month_value,self.due_day)
                }
            )
            month_value += self.pay_interval
            if month_value > 12:
                month_value-=12
                year_value+=1
        #make sure there isn't rounding problem like: the fraction -> 10/3 is 3.33 0.01 is missing
        #adding it to the last installment
        installments[-1]["amount"]+=round(pay_amount - pay_installment_amount*pay_installment_count, 2)
        receive_installment_count = self.receive_duration//self.receive_interval
        receive_amount = (self.amount + (self.amount*self.interest_rate/100 if self.type==OperationType.Fund else 0))
        receive_installment_amount = round( receive_amount / receive_installment_count, 2)
        year_value, month_value = self.receive_date.year, self.receive_date.month
        for _ in range(receive_installment_count):
            installments.append(
                {
                "type": InstallmentType.Receive,
                "amount": receive_installment_amount,
                "date": date(year_value,month_value,self.due_day)
                }
            )
            month_value += self.receive_interval
            while month_value > 12:
                month_value-=12
                year_value+=1
        #make sure there isn't rounding problem like: the fraction -> 10/3 is 3.33 0.01 is missing
        #adding it to the last installment
        installments[-1]["amount"]+=round(receive_amount - receive_installment_amount*receive_installment_count, 2)
        return installments

class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='from_transactions')
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to_transactions')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Installment(models.Model):
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name = 'installments')
    type = models.IntegerField(choices=InstallmentType)
    amount = models.DecimalField(max_digits = 14, decimal_places=2)
    date = models.DateField()
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True, blank=True)
    completed = models.BooleanField(default=False)

