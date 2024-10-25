from django.db import models
from django_access_point.models import TenantBase, UserBase

class Tenant(TenantBase):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

class TenantUser(UserBase):
    phone_no = models.CharField(max_length=100)