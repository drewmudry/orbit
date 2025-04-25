from django.contrib import admin
from .models import Organization, Profile, Group, Membership

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'organization', 'is_admin')
    list_filter = ('organization', 'is_admin')
    search_fields = ('name', 'email')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    list_filter = ('organization',)
    search_fields = ('name',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('profile', 'group', 'is_admin', 'announce_can_create', 'sign_can_create')
    list_filter = ('group', 'is_admin', 'announce_can_create', 'sign_can_create')
    search_fields = ('profile__name', 'group__name')