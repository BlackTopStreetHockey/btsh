from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class User(AbstractUser):
    MALE = 'male'
    FEMALE = 'female'
    NON_BINARY = 'non_binary'
    GENDERS = {
        MALE: 'Male',
        FEMALE: 'Female',
        NON_BINARY: 'Non-binary',
    }

    gender = models.CharField(max_length=16, choices=GENDERS, null=True, blank=True)

    def __str__(self):
        return f'{self.get_full_name()} - {self.get_username()}'
