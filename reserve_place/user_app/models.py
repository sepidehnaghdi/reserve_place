from django.db import models
from django.contrib.auth.models import User, Group

from locator.models import LocatorProfile


class EmailConfirmation(models.Model):
    user = models.ForeignKey(User)
    confirmation_key = models.CharField(max_length=50, null=False, blank=False)
    expire_time = models.DateTimeField(null=False, blank=False)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         print("hereeeeee")
    #         group = self.user.groups.values_list('name', flat=True)[0]
    #
    #         if group == 'locator':
    #             LocatorProfile.objects.create(user=self.user)
    #             # elif group_dict['name'] == 'renter':
    #             #     from renter import RenterProfile
    #             #     RenterProfile.objects.create(user=user)
    #


