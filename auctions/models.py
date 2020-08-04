from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title} starting price: ${self.starting_bid}"