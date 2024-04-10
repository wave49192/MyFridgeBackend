from django.contrib.auth.models import AbstractUser
from django.db import models

from RecommendationSystem.models import Recipe


class User(AbstractUser):
    email = models.CharField(max_length=250, unique=True, null=False, blank=False)
    REGISTRATION_CHOICES = [
        ('email', 'Email'),
        ('google', 'Google'),
    ]
    registration_method = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='email'
    )
    favourite_recipes = models.ManyToManyField(Recipe, default=[], blank=True)

    def __str__(self):
       return self.username