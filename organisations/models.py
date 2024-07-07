from django.db import models
from django.conf import settings


class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='organisations')  # allows for user_instance.organisations.all()

    def __str__(self):
        return self.name
