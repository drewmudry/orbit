from django.db import models
from core.users.models import User

class Organization(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'organization')
    
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='groups')
    members = models.ManyToManyField(Profile, through='Membership', related_name='groups')
    
    def __str__(self):
        return self.name

class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    announce_can_create = models.BooleanField(default=False)
    sign_can_create = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('profile', 'group')
        
    def __str__(self):
        return f"{self.profile.name} in {self.group.name}"