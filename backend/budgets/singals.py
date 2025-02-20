from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Budget

@receiver(pre_delete, sender=User)
def save_user_name_before_delete(sender, instance, **kwargs):
    Budget.objects.filter(user=instance).update(user_name=instance.username)
