from django.db import models
from django.utils.translation import gettext_lazy as _

class InstallmentType(models.IntegerChoices):
    Pay = 1, _('Pay')
    Receive = 2, _('Receive')

class IntervalType(models.IntegerChoices):
    Monthly = 1, _('Monthly')
    Quarterly = 3, _('Quarterly')
    Semiannual = 6, _('Semiannual')
    Annual = 12, _('Annual')

class DurationType(models.IntegerChoices):
    d1month = 1, _('1 month')
    d3months = 3, _('3 months')
    d6months = 6, _('6 months')
    d9months = 9, _('9 months')
    d12months = 12, _('12 months')

class OperationType(models.IntegerChoices):
    Loan = 1, _('Loan')
    Fund = 2, _('Fund')
