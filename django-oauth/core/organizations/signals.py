from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.rabbit import publish_to_rabbitmq
from .models import Profile, Organization, Group, Membership

# Profile signals
@receiver(post_save, sender=Profile)
def profile_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    message = {
        'id': instance.id,
        'name': instance.name,
        'email': instance.email,
        'is_admin': instance.is_admin,
        'user_email': instance.user.email,
        'action': action
    }
    publish_to_rabbitmq('profile', message)

@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    message = {
        'id': instance.id,
        'name': instance.name,
        'email': instance.email,
        'is_admin': instance.is_admin,
        'user_email': instance.user.email,
        'action': 'deleted'
    }
    publish_to_rabbitmq('profile', message)

# Organization signals
@receiver(post_save, sender=Organization)
def organization_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    message = {
        'id': instance.id,
        'name': instance.name,
        'action': action
    }
    publish_to_rabbitmq('organization', message)

@receiver(post_delete, sender=Organization)
def organization_deleted(sender, instance, **kwargs):
    message = {
        'id': instance.id,
        'name': instance.name,
        'action': 'deleted'
    }
    publish_to_rabbitmq('organization', message)

# Group signals
@receiver(post_save, sender=Group)
def group_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    message = {
        'id': instance.id,
        'name': instance.name,
        'organization_id': instance.organization.id,
        'action': action
    }
    publish_to_rabbitmq('group', message)

@receiver(post_delete, sender=Group)
def group_deleted(sender, instance, **kwargs):
    message = {
        'id': instance.id,
        'name': instance.name,
        'organization_id': instance.organization.id,
        'action': 'deleted'
    }
    publish_to_rabbitmq('group', message)

# Membership signals
@receiver(post_save, sender=Membership)
def membership_saved(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    message = {
        'profile_id': instance.profile.id,
        'group_id': instance.group.id,
        'is_admin': instance.is_admin,
        'announce_can_create': instance.announce_can_create,
        'sign_can_create': instance.sign_can_create,
        'action': action
    }
    publish_to_rabbitmq('membership', message)

@receiver(post_delete, sender=Membership)
def membership_deleted(sender, instance, **kwargs):
    message = {
        'profile_id': instance.profile.id,
        'group_id': instance.group.id,
        'is_admin': instance.is_admin,
        'announce_can_create': instance.announce_can_create,
        'sign_can_create': instance.sign_can_create,
        'action': 'deleted'
    }
    publish_to_rabbitmq('membership', message) 