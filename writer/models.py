from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Writer(AbstractUser):
    name = models.CharField(max_length=50, null=True, blank=True)
    is_editor = models.BooleanField(default=False)
