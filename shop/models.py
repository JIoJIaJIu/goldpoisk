from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    admin = models.ForeignKey('Admin')
    manager = models.ForeignKey('Manager')

class Admin(User):
    pass

class Manager(models.Model):
    pass
