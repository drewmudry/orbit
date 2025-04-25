from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.organizations'
    label = 'organizations'

    def ready(self):
        import core.organizations.signals  # noqa
