from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def create_initial_bank_instance(sender, **kwargs):
    from .models import Bank
    if Bank.objects.count() == 0:
        Bank.objects.create(balance = settings.BANK_START_BALANCE)

@receiver(post_migrate)
def create_initial_bank_user_instance(sender, **kwargs):
    User = get_user_model()
    if User.objects.filter(is_superuser=True).count() == 0:
        User.objects.create_superuser(username='admin', email='admin@bank.com', password='admin')

