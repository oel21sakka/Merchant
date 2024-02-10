from django.contrib import admin
from .models import Operation, Installment, Transaction

admin.site.register([Operation,Installment,Transaction])