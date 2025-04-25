from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.rabbit import publish_to_rabbitmq
from .models import User

@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    message = {
        'id': instance.id,
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'is_active': instance.is_active,
        'is_staff': instance.is_staff,
        'action': action
    }
    publish_to_rabbitmq('user', message)

@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    message = {
        'id': instance.id,
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'is_active': instance.is_active,
        'is_staff': instance.is_staff,
        'action': 'deleted'
    }
    publish_to_rabbitmq('user', message) 