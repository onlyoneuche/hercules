from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string


class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='organisations')  # allows for user_instance.organisations.all()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.orgId:
            self.userId = get_random_string(length=32)
        super().save(*args, **kwargs)
