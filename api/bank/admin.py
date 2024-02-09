from django.contrib import admin
from .models import Bank,Loan

admin.site.register([Bank,Loan])