# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Package

@receiver(post_save, sender=Package)
def update_completed_at(sender, instance, created, **kwargs):
    if instance.status == 'completed' and not instance.completed_at:
        instance.completed_at = timezone.now()
        instance.save()

@receiver(post_save, sender=Package)
def update_received_at(sender, instance, created, **kwargs):
    if instance.status == 'ready_for_pickup' and not instance.received_at:
        instance.received_at = timezone.now()
        instance.save()