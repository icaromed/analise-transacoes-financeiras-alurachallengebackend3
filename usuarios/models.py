from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    deleted = models.BooleanField(default=False)
