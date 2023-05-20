from django.contrib.auth.models import User
from django.db import models

from alert.constants import CREATED, TRIGGERED, DELETED


# Create your models here.
class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    currency = models.CharField(max_length=10, blank=False, null=False)
    limit = models.DecimalField(max_digits=15, decimal_places=4)
    status = models.CharField(choices=[(CREATED, CREATED),
                                       (TRIGGERED, TRIGGERED),
                                       (DELETED, DELETED)],
                              default=CREATED, max_length=10)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username + " " + str(self.limit) + " " + self.currency
