from django.db import models

class Role(models.TextChoices):
    MEMBER = 'member', 'Member'
    MANAGER = 'manager', 'Manager'
    ADMIN = 'admin', 'Admin'

