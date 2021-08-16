from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, DO_NOTHING, DecimalField, DateField, BooleanField)
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
