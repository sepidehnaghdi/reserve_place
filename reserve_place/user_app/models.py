from django.db import models
from django.contrib.auth.models import User, Group

from locator.models import LocatorProfile


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User)
    confirmation_key = models.CharField(max_length=50, null=False, blank=False)
    expire_time = models.DateTimeField(null=False, blank=False)

